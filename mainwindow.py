import sys
import yfinance as yf
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui_mainwindow import Ui_MainWindow
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator, DateFormatter

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(left=0.1, bottom=0.15)  # Adjust margins
        super().__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set up the canvas for plotting
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout = QVBoxLayout(self.ui.plotWidget)
        layout.addWidget(self.canvas)

        # Set initial dates
        self.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.ui.endDateEdit.setDate(QDate.currentDate())

        # Connect the download button to the function
        self.ui.downloadButton.clicked.connect(self.download_and_plot_data)

        # Connect the dropdown to the function that updates the plot
        self.ui.ETF_Dropdown.currentIndexChanged.connect(self.update_plot)

    def download_and_plot_data(self):
        # Get the start date and end date
        start_date = self.ui.startDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.ui.endDateEdit.date().toString("yyyy-MM-dd")

        # Get all symbols in the dropdown
        symbols = [self.ui.ETF_Dropdown.itemText(i) for i in range(self.ui.ETF_Dropdown.count())]

        # Download and save data for all symbols
        for ticker in symbols:
            data = self.download_data(ticker, start_date, end_date)
            self.save_data_to_json(data, ticker)

        # Plot data for the selected symbol
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        self.plot_data(selected_ticker)

    def download_data(self, ticker, start_date, end_date):
        return yf.download(ticker, start=start_date, end=end_date)

    def save_data_to_json(self, data, ticker):
        data_to_save = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data_to_save.reset_index(inplace=True)
        data_to_save['Date'] = data_to_save['Date'].dt.strftime('%Y-%m-%d')
        data_to_save.to_json(f"{ticker}_data.json", orient="records", date_format="iso")

    def plot_data(self, ticker):
        # Load data from JSON file
        data = pd.read_json(f"{ticker}_data.json", orient="records")
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        self.canvas.axes.clear()
        self.canvas.axes.plot(data.index, data['Close'])

        # Customize the x-axis
        locator = AutoDateLocator()
        formatter = DateFormatter('%Y-%m')
        self.canvas.axes.xaxis.set_major_locator(locator)
        self.canvas.axes.xaxis.set_major_formatter(formatter)

        # Rotate the date labels
        self.canvas.axes.tick_params(axis='x', rotation=45)

        # Add grid lines
        self.canvas.axes.grid(True)

        # Set title and labels
        self.canvas.axes.set_title(f"{ticker} Stock Price")
        self.canvas.axes.set_xlabel("Date")
        self.canvas.axes.set_ylabel("Close Price")

        # Check if the yAxisCheckbox is checked
        if self.ui.yAxisCheckbox.isChecked():
            # Calculate the maximum y-axis value across all symbols
            max_y_value = self.calculate_max_y_value()
            self.canvas.axes.set_ylim(top=max_y_value)

        self.canvas.draw()

    def calculate_max_y_value(self):
        # Get all symbols in the dropdown
        symbols = [self.ui.ETF_Dropdown.itemText(i) for i in range(self.ui.ETF_Dropdown.count())]

        max_y_value = 0
        for ticker in symbols:
            data = pd.read_json(f"{ticker}_data.json", orient="records")
            max_y_value = max(max_y_value, data['Close'].max())

        return max_y_value

    def update_plot(self):
        # Get the selected symbol from the dropdown
        selected_ticker = self.ui.ETF_Dropdown.currentText()
        # Plot data for the selected symbol
        self.plot_data(selected_ticker)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())