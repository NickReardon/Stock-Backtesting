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
        all_data = []

        for ticker in self.symbols:
            data = yf.download(ticker, start=self.start_date, end=self.end_date)
            data_to_save = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data_to_save.reset_index(inplace=True)
            data_to_save['Date'] = data_to_save['Date'].dt.strftime('%Y-%m-%d')
            data_to_save['Symbol'] = ticker  # Add the symbol to each entry
            all_data.append(data_to_save)

        # Combine all data into a single DataFrame
        combined_data = pd.concat(all_data, ignore_index=True)

        # Save the combined data to a single JSON file
        combined_data.to_json("all_symbols_data.json", orient="records", date_format="iso")

        self.download_complete.emit()