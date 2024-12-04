import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QTableWidgetItem, QTableWidget, QTableView, QHeaderView, QDialog, QLabel
from PySide6.QtCore import QDate, QTimer, QThread, Signal, QCoreApplication, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from plot_utils import plot_stock_price, plot_buy_sell_signals, DATE_FORMAT, AXIS_FONT_SIZE, TITLE_FONT_SIZE, X_AXIS_TICK_FONT_SIZE, NUMBER_OF_TICKS
from mainwindow_ui import Ui_MainWindow
from backtest_ui import Ui_Backtest
from mpl_canvas import MplCanvas
from strategy import strategies, DownloadThread
from pubsub import PubSub
import random


# Define constants for date format, axis font size, number of ticks, and margins
DATE_FORMAT = '%m/%y'
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
X_AXIS_TICK_FONT_SIZE = 8
NUMBER_OF_TICKS = 24
LEFT_MARGIN_SMALL = 0.075
LEFT_MARGIN_LARGE = 0.12
RIGHT_MARGIN_SMALL = 0.05
RIGHT_MARGIN_LARGE = 0.1
TOP_MARGIN_SMALL = 0.05
TOP_MARGIN_LARGE = 0.1
BOTTOM_MARGIN_LARGE = 0.2
BOTTOM_MARGIN_SMALL = 0.1



class BacktestWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Backtest()
        self.ui.setupUi(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set up the canvas for plotting
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout = QVBoxLayout(self.ui.plotWidget)
        layout.addWidget(self.canvas)

        self.initialize_ui()
        self.initialize_blank_plot()

        self.download_completed = False




        self.pubsub = PubSub()
        self.pubsub.subscribe("price_update", self.update_live_price)

        # Simulate live price updates
        self.simulate_live_price_updates()

        # Update the status bar immediately
        self.update_live_price(0, 0)

    def simulate_live_price_updates(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_and_generate_fake_price_update)
        self.timer.start(5000)  # Update every 5 seconds

    def check_and_generate_fake_price_update(self):
        if self.download_completed:
            self.generate_fake_price_update()

    def generate_fake_price_update(self):
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        data = pd.read_json("all_symbols_data.json", orient="records")
        new_price = data.loc[data['Symbol'] == selected_ticker, 'Close'].iloc[-1]
        delta = random.gauss(-(new_price * 0.01), new_price * 0.01)  # Simulate a price change (delta) with a Gaussian distribution
        final_price = new_price + delta  # Apply the delta to the new price

        self.pubsub.notify("price_update", final_price, delta)

    def update_live_price(self, new_price, delta):
        color = "green" if delta >= 0 else "red"
        self.status_label.setText(f'<span style="color: {color};">Live Price: ${new_price:.2f} ({delta:+.2f})</span>')

        # region Initialization Methods
    def initialize_ui(self):
        """Initialize the UI components and connect signals to slots."""
        self.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.ui.endDateEdit.setDate(QDate.currentDate())
        self.ui.progressBar.setVisible(False)
        self.populate_strategy_combobox()
        self.ui.backtestButton.setEnabled(False)
        self.ui.downloadButton.clicked.connect(self.download_and_plot_data)
        self.ui.ETF_Dropdown.currentIndexChanged.connect(self.update_plot)
        self.ui.backtestButton.clicked.connect(self.open_backtest_window)
        self.ui.yAxisCheckbox.stateChanged.connect(self.update_plot)
        self.status_label = QLabel()
        self.status_label.setStyleSheet("padding-left:8px;background:rgba(255,255,255,255);color:black;font-weight:bold;")
        self.status_label.setText("Live Price: $0.00")
        self.statusBar().addWidget(self.status_label)

    def initialize_blank_plot(self):
        """Initialize the plot with blank x and y axes and no ticks."""
        self.canvas.axes.clear()
        self.canvas.axes.set_xlim(0, 1)
        self.canvas.axes.set_ylim(0, 1)
        self.canvas.axes.set_xticks([])
        self.canvas.axes.set_yticks([])
        self.canvas.axes.set_title("Market Data", fontsize=TITLE_FONT_SIZE)
        self.canvas.axes.set_xlabel("X-Axis")
        self.canvas.axes.set_ylabel("Y-Axis")
        self.canvas.draw()

    def populate_strategy_combobox(self):
        """Populate the strategyComboBox with strategy names."""
        self.ui.strategyComboBox.clear()
        for strategy_name in strategies.keys():
            self.ui.strategyComboBox.addItem(strategy_name)
    # endregion

    # region Data Download Methods
    def download_and_plot_data(self):
        """Start the data download and plot process."""
        self.AnimateProgressbar()
        start_date = self.ui.startDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.ui.endDateEdit.date().toString("yyyy-MM-dd")
        symbols = [self.ui.ETF_Dropdown.itemText(i) for i in range(self.ui.ETF_Dropdown.count())]
        self.initiate_download_thread(start_date, end_date, symbols)

    def initiate_download_thread(self, start_date, end_date, symbols):
        """Initiate the download thread for fetching data."""
        self.download_thread = DownloadThread(symbols, start_date, end_date, self)
        self.download_thread.download_complete.connect(self.on_download_complete)
        self.download_thread.start()

    def on_download_complete(self):
        """Handle actions after download is complete."""
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        self.plot_data(selected_ticker)
        QTimer.singleShot(500, self.complete_progress_bar)
        self.download_completed = True
        self.ui.backtestButton.setEnabled(True)

    def complete_progress_bar(self):
        """Complete the progress bar animation."""
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(1)
        self.ui.progressBar.setFormat("Complete")
        QTimer.singleShot(5000, lambda: self.ui.progressBar.setVisible(False))
    # endregion

    # region Plotting Methods
    def plot_data(self, ticker):
        """Plot the data for the selected ticker."""
        all_data = pd.read_json("all_symbols_data.json", orient="records")
        data = all_data[all_data['Symbol'] == ticker]
        data.loc[:, 'Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        self.canvas.axes.clear()
        for i in range(1, len(data)):
            color = 'green' if data['Close'].iloc[i] > data['Close'].iloc[i - 1] else 'red'
            self.canvas.axes.plot(data.index[i-1:i+1], data['Close'].iloc[i-1:i+1], color=color)

        if self.ui.yAxisCheckbox.isChecked():
            max_y_value = self.calculate_max_y_value(all_data['Symbol'].unique())
            self.canvas.axes.set_ylim(0, max_y_value*1.1)

        self.customize_plot(self.canvas.axes, ticker, "Stock Price")
        self.canvas.draw()

    def calculate_max_y_value(self, symbols):
        """Calculate the maximum y-axis value across all symbols."""
        max_y_value = 0
        for ticker in symbols:
            data = pd.read_json("all_symbols_data.json", orient="records")
            data = data[data['Symbol'] == ticker]
            max_y_value = max(max_y_value, data['Close'].max())
        return max_y_value

    def update_plot(self):
        """Update the plot based on the selected symbol."""
        if not self.download_completed:
            print("Download not completed yet. Plot update skipped.")
            return
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        self.plot_data(selected_ticker)

    def customize_plot(self, ax, ticker, title):
        """Customize the plot with labels, grid, and formatting."""
        locator = AutoDateLocator(maxticks={
            'YEARLY': NUMBER_OF_TICKS,
            'MONTHLY': NUMBER_OF_TICKS,
            'DAILY': NUMBER_OF_TICKS,
            'HOURLY': NUMBER_OF_TICKS,
            'MINUTELY': NUMBER_OF_TICKS,
            'SECONDLY': NUMBER_OF_TICKS
        })
        formatter = DateFormatter(DATE_FORMAT)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))
        ax.tick_params(axis='x', rotation=45, labelsize=X_AXIS_TICK_FONT_SIZE)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.set_title(f"{ticker} {title}", fontsize=TITLE_FONT_SIZE)
        ax.set_xlabel("Date", fontsize=AXIS_FONT_SIZE)
        ax.set_ylabel("Price", fontsize=AXIS_FONT_SIZE)
        # ax.legend()
        ax.figure.subplots_adjust(bottom=0.17)
    # endregion

    # region Backtest Methods
    def open_backtest_window(self):
        """Open the backtest window and display the data."""
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        selected_strategy_name = self.ui.strategyComboBox.currentText()
        selected_strategy = strategies[selected_strategy_name]['strategy']
        run_backtest_algorithm(selected_ticker, selected_strategy)
        self.backtest_window = BacktestWindow(self)
        self.backtest_window.show()
        load_backtest_data(self.backtest_window)
        plot_strategy_performance(self.backtest_window, selected_ticker, selected_strategy_name)
    # endregion

    # region Progress Bar Methods
    def AnimateProgressbar(self):
        """Animate the progress bar during data download."""
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(0)
        QCoreApplication.processEvents()
    # endregion

def run_backtest_algorithm(symbol, strategy):
    """Run the selected backtest strategy."""
    strategy(symbol)
    results_log = pd.read_csv('results.csv')
    return results_log

def load_backtest_data(backtest_window):
    """Load and display the backtest data in the backtest window."""
    df = pd.read_csv('results.csv')
    df_data = df.iloc[:-1]
    df_results = df.iloc[-1:]

    backtest_window.ui.backtestTable.setRowCount(len(df_data))
    backtest_window.ui.backtestTable.setColumnCount(len(df_data.columns))
    backtest_window.ui.backtestTable.setHorizontalHeaderLabels(df_data.columns)

    for i, row in df_data.iterrows():
        for j, value in enumerate(row):
            if df_data.columns[j] == 'Date':
                value = pd.to_datetime(value).strftime('%d/%m/%Y')
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            elif df_data.columns[j] in ['Price', 'Transaction Amount', 'Gain/Loss', 'Balance']:
                value = f"${float(value):.2f}"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            elif df_data.columns[j] == 'Shares':
                value = f"{int(value)}"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            else:
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            backtest_window.ui.backtestTable.setItem(i, j, item)

    backtest_window.ui.backtestTable.resizeColumnsToContents()
    backtest_window.ui.backtestTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    backtest_window.ui.backtestTable.setMinimumSize(backtest_window.ui.backtestTable.sizeHint())

    model = QStandardItemModel(1, 4)
    model.setHorizontalHeaderLabels(["Total Gain/Loss", "Balance", "Total Return", "Annual Return"])

    for j, value in enumerate(df_results.iloc[0]):
        header_item = model.horizontalHeaderItem(j)
        if header_item:
            if header_item.text() in ["Total Gain/Loss", "Balance"]:
                value = f"${float(value):.2f}"
            elif header_item.text() in ["Total Return", "Annual Return"]:
                value = f"{float(value):.2f}%"
        item = QStandardItem(str(value))
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        model.setItem(0, j, item)

    backtest_window.ui.resultsTable.setModel(model)
    backtest_window.ui.resultsTable.resizeColumnsToContents()
    backtest_window.ui.resultsTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    backtest_window.ui.resultsTable.setMinimumSize(backtest_window.ui.resultsTable.sizeHint())

    while backtest_window.ui.resultsTable.model().columnCount() > 4:
        backtest_window.ui.resultsTable.model().removeColumn(4)

def plot_strategy_performance(backtest_window, ticker, strategy_name):
    """Plot the strategy performance in the backtest window."""
    data, transactions = load_data(ticker)
    if data.empty or transactions.empty:
        print("No data to plot.")
        return

    fig, canvas = setup_canvas(backtest_window)
    adjust_margins(fig)
    plot_function = strategies[strategy_name]['plot']
    if plot_function:
        plot_function(fig, data, transactions, ticker)
    canvas.draw()

def load_data(ticker):
    """Load data for the given ticker."""
    data = pd.read_json('all_symbols_data.json', convert_dates=True)
    data = data[data['Symbol'] == ticker]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    transactions = pd.read_csv('transactions.csv', parse_dates=['Date'])
    return data, transactions

def setup_canvas(backtest_window):
    """Set up the canvas for plotting in the backtest window."""
    fig = Figure(figsize=(10, 8), dpi=100)
    canvas = FigureCanvas(fig)
    layout = QVBoxLayout(backtest_window.ui.backtestPlot)
    layout.addWidget(canvas)
    return fig, canvas

def adjust_margins(fig):
    """Adjust margins based on the current size of the canvas."""
    width, height = fig.get_size_inches() * fig.dpi
    left_margin = LEFT_MARGIN_LARGE if width < 800 else LEFT_MARGIN_SMALL
    right_margin = RIGHT_MARGIN_LARGE if width < 800 else RIGHT_MARGIN_SMALL
    top_margin = TOP_MARGIN_LARGE if height < 600 else TOP_MARGIN_SMALL
    bottom_margin = BOTTOM_MARGIN_LARGE if height < 600 else BOTTOM_MARGIN_SMALL
    fig.subplots_adjust(left=left_margin, bottom=bottom_margin, right=1-right_margin, top=1-top_margin)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())