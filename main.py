import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QProgressBar, QTableWidgetItem, QTableWidget, QTableView, QHeaderView, QSizePolicy
from PySide6.QtCore import QDate, QTimer, QThread, Signal, QCoreApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MultipleLocator, MaxNLocator
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from plot_utils import plot_stock_price, plot_buy_sell_signals, DATE_FORMAT, AXIS_FONT_SIZE, TITLE_FONT_SIZE, X_AXIS_TICK_FONT_SIZE, NUMBER_OF_TICKS
from mainwindow_ui import Ui_MainWindow
from backtest import BacktestWindow
from mpl_canvas import MplCanvas
from strategy import strategies, DownloadThread

# Define variables for date format, axis font size, and number of ticks
DATE_FORMAT = '%m/%y'  # Default date format
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
X_AXIS_TICK_FONT_SIZE = 8  # Font size for x-axis ticks
NUMBER_OF_TICKS = 24       # Number of ticks on the x-axis

# Define variables for margins and font sizes
LEFT_MARGIN_SMALL = 0.075
LEFT_MARGIN_LARGE = 0.12
RIGHT_MARGIN_SMALL = 0.05
RIGHT_MARGIN_LARGE = 0.1
TOP_MARGIN_SMALL = 0.05
TOP_MARGIN_LARGE = 0.1
BOTTOM_MARGIN_SMALL = 0.1
BOTTOM_MARGIN_LARGE = 0.2

# region Backtest Methods
def run_backtest_algorithm(symbol, strategy):
    # Run the selected strategy
    strategy(symbol)

    # Read the results log from the CSV file
    results_log = pd.read_csv('results.csv')

    return results_log

def load_backtest_data(backtest_window):
    # Load and display the backtest data in the backtest window
    print("Loading backtest data...")

    # Load the results CSV file
    df = pd.read_csv('results.csv')
    
    # Separate the last row as results
    df_data = df.iloc[:-1]
    df_results = df.iloc[-1:]

    # Display main data
    backtest_window.ui.backtestTable.setRowCount(len(df_data))
    backtest_window.ui.backtestTable.setColumnCount(len(df_data.columns))
    backtest_window.ui.backtestTable.setHorizontalHeaderLabels(df_data.columns)

    for i, row in df_data.iterrows():
        for j, value in enumerate(row):
            # Format date to dd/mm/yyyy
            if df_data.columns[j] == 'Date':
                value = pd.to_datetime(value).strftime('%d/%m/%Y')
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center-justify the text
            # Format dollar amounts to 2 decimal points with a dollar sign
            elif df_data.columns[j] in ['Price', 'Transaction Amount', 'Gain/Loss', 'Balance']:
                value = f"${float(value):.2f}"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Right-justify the text
            elif df_data.columns[j] == 'Shares':
                value = f"{int(value)}"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Right-justify the text
            else:
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center-justify the text
            backtest_window.ui.backtestTable.setItem(i, j, item)

    # Resize columns to fit the content
    backtest_window.ui.backtestTable.resizeColumnsToContents()

    # Adjust the size of the table to fit its contents
    backtest_window.ui.backtestTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    backtest_window.ui.backtestTable.setMinimumSize(backtest_window.ui.backtestTable.sizeHint())

    # Display results using QStandardItemModel
    model = QStandardItemModel(1, 4)  # 4 columns for the results table
    model.setHorizontalHeaderLabels(["Total Gain/Loss", "Balance", "Total Return", "Annual Return"])

    for j, value in enumerate(df_results.iloc[0]):
        header_item = model.horizontalHeaderItem(j)
        if header_item:
            if header_item.text() in ["Total Gain/Loss", "Balance"]:
                value = f"${float(value):.2f}"
            elif header_item.text() in ["Total Return", "Annual Return"]:
                value = f"{float(value):.2f}%"
        item = QStandardItem(str(value))
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Right-justify the text
        model.setItem(0, j, item)

    backtest_window.ui.resultsTable.setModel(model)
    backtest_window.ui.resultsTable.resizeColumnsToContents()

    # Adjust the size of the table to fit its contents
    backtest_window.ui.resultsTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    backtest_window.ui.resultsTable.setMinimumSize(backtest_window.ui.resultsTable.sizeHint())

    # Remove any columns after the 4th in the backtest table
    while backtest_window.ui.resultsTable.model().columnCount() > 4:
        backtest_window.ui.resultsTable.model().removeColumn(4)
# endregion

# region Plotting Methods
def plot_strategy_performance(backtest_window, ticker, strategy_name):
    data, transactions = load_data(ticker)
    if data.empty or transactions.empty:
        print("No data to plot.")
        return

    fig, canvas = setup_canvas(backtest_window)
    adjust_margins(fig)

    # Get the plot function from the strategy
    plot_function = strategies[strategy_name]['plot']
    if plot_function:
        plot_function(fig, data, transactions, ticker)  # Pass data and transactions



    canvas.draw()

def load_data(ticker):
    data = pd.read_json('all_symbols_data.json', convert_dates=True)
    data = data[data['Symbol'] == ticker]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    transactions = pd.read_csv('transactions.csv', parse_dates=['Date'])

    print("Filtered Data Head:", data.head())
    print("Transactions Head:", transactions.head())

    return data, transactions

def setup_canvas(backtest_window):
    fig = Figure(figsize=(10, 8), dpi=100)
    canvas = FigureCanvas(fig)
    layout = QVBoxLayout(backtest_window.ui.backtestPlot)
    layout.addWidget(canvas)
    return fig, canvas

def adjust_margins(fig):
    # Adjust margins based on the current size of the canvas
    width, height = fig.get_size_inches() * fig.dpi
    left_margin = LEFT_MARGIN_LARGE if width < 800 else LEFT_MARGIN_SMALL
    right_margin = RIGHT_MARGIN_LARGE if width < 800 else RIGHT_MARGIN_SMALL
    top_margin = TOP_MARGIN_LARGE if height < 600 else TOP_MARGIN_SMALL
    bottom_margin = BOTTOM_MARGIN_LARGE if height < 600 else BOTTOM_MARGIN_SMALL
    fig.subplots_adjust(left=left_margin, bottom=bottom_margin, right=1-right_margin, top=1-top_margin)

def customize_plot(ax, ticker, strategy_name):
    # Increase the number of ticks on the x-axis
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
    
    # Ensure a consistent number of ticks (e.g., 24 ticks)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))

    # Rotate the date labels and set font size
    ax.tick_params(axis='x', rotation=45, labelsize=X_AXIS_TICK_FONT_SIZE)

    # Add grid lines
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Set title and labels
    ax.set_title(f"{ticker} {strategy_name} Strategy Performance", fontsize=TITLE_FONT_SIZE)
    ax.set_xlabel("Date", fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel("Price", fontsize=AXIS_FONT_SIZE)
    
    # Add legend
    ax.legend()
    
    # Adjust the bottom margin
    ax.figure.subplots_adjust(bottom=0.17)
# endregion

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

        self.download_completed = False  # Add this flag

    # region Initialization Methods
    def initialize_ui(self):
        # Set initial dates
        self.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.ui.endDateEdit.setDate(QDate.currentDate())

        # Initialize progress bar to be invisible
        self.ui.progressBar.setVisible(False)

        # Populate strategyComboBox
        self.populate_strategy_combobox()\
        
        # Disable the backtest button initially
        self.ui.backtestButton.setEnabled(False)

        # Connect UI components to their respective functions
        self.ui.downloadButton.clicked.connect(self.download_and_plot_data)
        self.ui.ETF_Dropdown.currentIndexChanged.connect(self.update_plot)
        self.ui.backtestButton.clicked.connect(self.open_backtest_window)
        self.ui.yAxisCheckbox.stateChanged.connect(self.update_plot)  # Connect checkbox state change to update_plot

    def initialize_blank_plot(self):
        # Initialize the plot with blank x and y axes and no ticks
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
        # Populate the strategyComboBox with strategy names
        self.ui.strategyComboBox.clear()  # Clear existing items
        for strategy_name in strategies.keys():
            self.ui.strategyComboBox.addItem(strategy_name)
    # endregion

    # region Event Handlers
    def resizeEvent(self, event):
        # Adjust margins when the window is resized
        self.canvas.adjust_margins()
        self.canvas.draw()
        super().resizeEvent(event)
    # endregion

    # region Data Download Methods
    def download_and_plot_data(self):
        # Make the progress bar visible and animate it
        self.AnimateProgressbar()

        # Get the start date and end date
        start_date = self.ui.startDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.ui.endDateEdit.date().toString("yyyy-MM-dd")

        # Get all symbols in the dropdown
        symbols = [self.ui.ETF_Dropdown.itemText(i) for i in range(self.ui.ETF_Dropdown.count())]

        print("1Downloading data...")

        # Start the download in a separate thread
        self.initiate_download_thread(start_date, end_date, symbols)

    def initiate_download_thread(self, start_date, end_date, symbols):
        self.download_thread = DownloadThread(symbols, start_date, end_date, self)
        self.download_thread.download_complete.connect(self.on_download_complete)
        self.download_thread.start()

    def on_download_complete(self):
        # Plot data for the selected symbol
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        self.plot_data(selected_ticker)

        # Stop the progress bar animation and set it to "Complete" after a delay
        QTimer.singleShot(500, self.complete_progress_bar)

        self.download_completed = True  # Set the flag
        
        self.ui.backtestButton.setEnabled(True)

    def complete_progress_bar(self):
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(1)
        self.ui.progressBar.setFormat("Complete")

        # Hide the progress bar after 5 seconds
        QTimer.singleShot(5000, lambda: self.ui.progressBar.setVisible(False))
    # endregion

    # region Plotting Methods
    def plot_data(self, ticker):
        # Load data from the combined JSON file
        all_data = pd.read_json("all_symbols_data.json", orient="records")
        
        # Filter data for the selected symbol
        data = all_data[all_data['Symbol'] == ticker]
        data.loc[:, 'Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        self.canvas.axes.clear()

        # Plot the data with different colors for positive and negative slopes
        for i in range(1, len(data)):
            color = 'green' if data['Close'].iloc[i] > data['Close'].iloc[i - 1] else 'red'
            self.canvas.axes.plot(data.index[i-1:i+1], data['Close'].iloc[i-1:i+1], color=color)

        # Customize the x-axis
        locator = AutoDateLocator()
        formatter = DateFormatter(DATE_FORMAT)
        self.canvas.axes.xaxis.set_major_locator(locator)
        self.canvas.axes.xaxis.set_major_formatter(formatter)

        # Ensure a consistent number of ticks (e.g., 24 ticks)
        self.canvas.axes.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))

        # Rotate the date labels and set font size
        self.canvas.axes.tick_params(axis='x', rotation=45, labelsize=X_AXIS_TICK_FONT_SIZE)

        # Add grid lines
        self.canvas.axes.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Set title and labels
        self.canvas.axes.set_title(f"{ticker} Stock Price", fontsize=TITLE_FONT_SIZE)
        self.canvas.axes.set_xlabel("Date", fontsize=AXIS_FONT_SIZE)
        self.canvas.axes.set_ylabel("Close Price", fontsize=AXIS_FONT_SIZE)

        # Check if the yAxisCheckbox is checked
        if self.ui.yAxisCheckbox.isChecked():
            # Calculate the maximum y-axis value across all symbols
            symbols = [self.ui.ETF_Dropdown.itemText(i) for i in range(self.ui.ETF_Dropdown.count())]
            max_y_value = self.calculate_max_y_value(symbols)
            self.canvas.axes.set_ylim(top=max_y_value)

        self.canvas.draw()

    def calculate_max_y_value(self, symbols):
        max_y_value = 0
        for ticker in symbols:
            data = pd.read_json("all_symbols_data.json", orient="records")
            data = data[data['Symbol'] == ticker]
            max_y_value = max(max_y_value, data['Close'].max())

        return max_y_value

    def update_plot(self):
        if not self.download_completed:
            print("Download not completed yet. Plot update skipped.")
            return

        # Get the selected symbol from the dropdown
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        # Plot data for the selected symbol
        self.plot_data(selected_ticker)
    # endregion

    # region Backtest Methods
    def open_backtest_window(self):
        # Get the selected symbol from the dropdown
        selected_ticker = self.ui.ETF_Dropdown.currentText()

        # Get the selected strategy from the strategyComboBox
        selected_strategy_name = self.ui.strategyComboBox.currentText()
        selected_strategy = strategies[selected_strategy_name]['strategy']  # Access the 'strategy' key

        # Run the backtest algorithm for the selected symbol and strategy
        run_backtest_algorithm(selected_ticker, selected_strategy)

        # Open the backtest window and display the data
        self.backtest_window = BacktestWindow(self)
        self.backtest_window.show()
        load_backtest_data(self.backtest_window)

        # Plot the strategy performance in the backtest window
        plot_strategy_performance(self.backtest_window, selected_ticker, selected_strategy_name)
    # endregion

    # region Progress Bar Methods
    def AnimateProgressbar(self):
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(0)

        # Process events to ensure the progress bar starts animating
        QCoreApplication.processEvents()
    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())