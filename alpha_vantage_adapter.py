import pandas as pd
import requests
from data_access import DataAccessInterface

class AlphaVantageAdaptee:
    def fetch_data(self, symbol, function, outputsize='full'):
        url = f"https://www.alphavantage.co/query"
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": "9NVDVP4A9JYY8IFN",
            "outputsize": outputsize,
            "datatype": "json"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Debugging: Print the JSON response
        json_response = response.json()
        print("JSON response:", json_response)
        
        # Extract the time series data
        time_series_key = 'Time Series (Daily)'
        if time_series_key not in json_response:
            raise ValueError(f"Expected key '{time_series_key}' not found in the response.")
        
        data = pd.DataFrame.from_dict(json_response[time_series_key], orient='index')
        
        # Rename columns to match the expected format
        data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        }, inplace=True)
        
        # Reset the index to make 'Date' a column
        data.reset_index(inplace=True)
        data.rename(columns={'index': 'Date'}, inplace=True)
        
        # Convert 'Date' to datetime format
        data['Date'] = pd.to_datetime(data['Date'])
        
        return data

    def save_to_csv(self, data, filename):
        data.to_csv(filename, index=False)

    def save_to_json(self, data, filename):
        data.to_json(filename, orient="records", date_format="iso")

class AlphaVantageAdapter(DataAccessInterface):
    def __init__(self):
        self.adaptee = AlphaVantageAdaptee()

    def fetch_data(self, symbol, start_date, end_date):
        data = self.adaptee.fetch_data(symbol, "TIME_SERIES_DAILY", outputsize='full')
        filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
        print(filtered_data)
        return filtered_data

    def save_data(self, data, filename):
        self.adaptee.save_to_csv(data, filename)

    def save_data_as_json(self, data, filename):
        self.adaptee.save_to_json(data, filename)