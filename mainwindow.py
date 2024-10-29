import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QProgressBar, QTableWidgetItem, QTableWidget, QTableView, QHeaderView
from PySide6.QtCore import QDate, QTimer, QThread, Signal, QCoreApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MultipleLocator, MaxNLocator
from mainwindow_ui import Ui_MainWindow
from backtest import BacktestWindow
from mpl_canvas import MplCanvas
from download_thread import DownloadThread
from backtest_logic import run_backtest_algorithm, load_backtest_data, plot_strategy_performance
from strats import strategies  # Import strategies

# Define variables for date format, axis font size, and number of ticks
DATE_FORMAT = '%m/%y'  # Default date format
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
X_AXIS_TICK_FONT_SIZE = 8  # Font size for x-axis ticks
NUMBER_OF_TICKS = 24       # Number of ticks on the x-axis

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

    def initialize_ui(self):
        # Set initial dates
        self.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.ui.endDateEdit.setDate(QDate.currentDate())

        # Initialize progress bar to be invisible
        self.ui.progressBar.setVisible(False)

        # Populate strategyComboBox
        self.populate_strategy_combobox()

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
        for strategy_name in strategies.keys():
            self.ui.strategyComboBox.addItem(strategy_name)

    def resizeEvent(self, event):
        # Adjust margins when the window is resized
        self.canvas.adjust_margins()
        self.canvas.draw()
        super().resizeEvent(event)

    def download_and_plot_data(self):
        # Make the progress bar visible and animate it
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(0)

        # Process events to ensure the progress bar starts animating
        QCoreApplication.processEvents()

        # Get the start date and end date
        start_date = self.ui.startDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.ui.endDateEdit.date().toString("yyyy-MM-dd")

        # Get all symbols in the dropdown
        symbols = [self.ui.ETF_Dropdown.itemText(i) for i in range(self.ui.ETF_Dropdown.count())]

        # Start the download in a separate thread
        self.download_thread = DownloadThread(symbols, start_date, end_date)
        self.download_thread.download_complete.connect(self.on_download_complete)
        self.download_thread.start()

    def on_download_complete(self):
        # Plot data for the selected symbol
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        self.plot_data(selected_ticker)

        # Stop the progress bar animation and set it to "Complete" after a delay
        QTimer.singleShot(500, self.complete_progress_bar)

    def complete_progress_bar(self):
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(1)
        self.ui.progressBar.setFormat("Complete")

        # Hide the progress bar after 5 seconds
        QTimer.singleShot(5000, lambda: self.ui.progressBar.setVisible(False))

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
        # Get the selected symbol from the dropdown
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        # Plot data for the selected symbol
        self.plot_data(selected_ticker)

    def open_backtest_window(self):
        # Get the selected symbol from the dropdown
        selected_ticker = self.ui.ETF_Dropdown.currentText()

        # Get the selected strategy from the strategyComboBox
        selected_strategy_name = self.ui.strategyComboBox.currentText()
        selected_strategy = strategies[selected_strategy_name]

        # Run the backtest algorithm for the selected symbol and strategy
        run_backtest_algorithm(selected_ticker, selected_strategy)

        # Open the backtest window and display the data
        self.backtest_window = BacktestWindow(self)
        self.backtest_window.show()
        load_backtest_data(self.backtest_window)

        # Plot the strategy performance in the backtest window
        plot_strategy_performance(self.backtest_window, selected_ticker, selected_strategy_name)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())