import sys
import yfinance as yf
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui_mainwindow import Ui_MainWindow
import matplotlib.dates as mdates

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
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

        # Connect the download button to the function
        self.ui.downloadButton.clicked.connect(self.download_and_plot_data)

    def download_and_plot_data(self):
        # Get the selected ETF, start date, and end date
        ticker = self.ui.ETF_Dropdown.currentText()
        start_date = self.ui.startDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.ui.endDateEdit.date().toString("yyyy-MM-dd")

        # Download data from yfinance
        data = self.download_data(ticker, start_date, end_date)

        # Save the data to a JSON file
        self.save_data_to_json(data, ticker)

        # Plot the data
        self.plot_data(data, ticker)

    def download_data(self, ticker, start_date, end_date):
        return yf.download(ticker, start=start_date, end=end_date)

    def save_data_to_json(self, data, ticker):
        data_to_save = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data_to_save.reset_index(inplace=True)
        data_to_save['Date'] = data_to_save['Date'].dt.strftime('%Y-%m-%d')
        data_to_save.to_json(f"{ticker}_data.json", orient="records", date_format="iso")

    def plot_data(self, data, ticker):
        # Load data from JSON file
        data = pd.read_json(f"{ticker}_data.json", orient="records")
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        self.canvas.axes.clear()
        self.canvas.axes.plot(data.index, data['Close'])

        # Customize the x-axis
        self.canvas.axes.xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to months
        self.canvas.axes.xaxis.set_minor_locator(mdates.WeekdayLocator())  # Set minor ticks to weekdays
        self.canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format the date labels

        # Rotate the date labels
        self.canvas.axes.tick_params(axis='x', rotation=45)

        # Add grid lines
        self.canvas.axes.grid(True)

        # Set title and labels
        self.canvas.axes.set_title(f"{ticker} Stock Price")
        self.canvas.axes.set_xlabel("Date")
        self.canvas.axes.set_ylabel("Close Price")

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())