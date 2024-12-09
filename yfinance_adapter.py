# yfinance_adapter.py

import yfinance as yf
import pandas as pd
from data_access import DataAccessInterface

class YFinanceAdaptee:
    def download_data(self, symbol, start_date, end_date):
        return yf.download(symbol, start=start_date, end=end_date)

    def save_to_csv(self, data, filename):
        data.to_csv(filename)

    def save_to_json(self, data, filename):
        data.to_json(filename, orient="records", date_format="iso")

class YFinanceAdapter(DataAccessInterface):
    def __init__(self):
        self.adaptee = YFinanceAdaptee()

    def fetch_data(self, symbol, start_date, end_date):
        return self.adaptee.download_data(symbol, start_date, end_date)

    def save_data(self, data, filename):
        self.adaptee.save_to_csv(data, filename)

    def save_data_as_json(self, data, filename):
        self.adaptee.save_to_json(data, filename)