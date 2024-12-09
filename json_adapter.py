# json_adapter.py

import pandas as pd
from data_access import DataAccessInterface

class JSONAdapter(DataAccessInterface):
    def __init__(self):
        self.adaptee = JSONAdaptee()

    def fetch_data(self, symbol, start_date, end_date):
        data = self.adaptee.read_json('all_symbols_data.json')
        data = data[data['Symbol'] == symbol]
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        return data

    def save_data(self, data, filename):
        self.adaptee.save_to_json(data, filename)


class JSONAdaptee:
    def read_json(self, filename):
        return pd.read_json(filename)

    def save_to_json(self, data, filename):
        data.to_json(filename, orient="records", date_format="iso")