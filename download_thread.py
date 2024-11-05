import yfinance as yf
import pandas as pd
from PySide6.QtCore import QThread, Signal

class DownloadThread(QThread):
    download_complete = Signal()

    def __init__(self, symbols, start_date, end_date, parent=None):
        super().__init__(parent)
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date

    def run(self):

        print("2Downloading data...")

        all_data = []
        print("3Downloading data...")

        for ticker in self.symbols:
            print("Entered loop")

            data = yf.download(ticker, start=self.start_date, end=self.end_date)
            print("Downloaded data for ticker")


            data_to_save = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            print("data chosen for saving")


            data_to_save.reset_index(inplace=True)
            print("data reset")


            data_to_save['Date'] = data_to_save['Date'].dt.strftime('%Y-%m-%d')
            print("data formatted")


            data_to_save['Symbol'] = ticker  # Add the symbol to each entry
            print("data symbol added")


            all_data.append(data_to_save)
            print("data appended")

        # Combine all data into a single DataFrame
        combined_data = pd.concat(all_data, ignore_index=True)
        print("Combined data")

        # Save the combined data to a single JSON file
        combined_data.to_json("all_symbols_data.json", orient="records", date_format="iso")
        print("Data downloaded and saved to all_symbols_data.json")

        self.download_complete.emit()