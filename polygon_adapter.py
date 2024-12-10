# polygon_adapter.py

import requests
import pandas as pd
from data_access import DataAccessInterface
from datetime import datetime, timedelta

class PolygonAdaptee:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_data(self, symbol, start_date, end_date):
        # Convert start_date and end_date to datetime objects
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

        # Calculate the total number of days in the date range
        total_days = (end_date_dt - start_date_dt).days

        # Define the maximum number of days per request as 1/5 of the total date range
        max_days = max(1, total_days // 5)

        # Initialize an empty DataFrame to store the combined results
        combined_df = pd.DataFrame()

        # Loop through the date range and make multiple requests, starting from the end date
        while end_date_dt > start_date_dt:
            # Calculate the start date for the current chunk
            chunk_start_date_dt = max(end_date_dt - timedelta(days=max_days), start_date_dt)
            chunk_start_date = chunk_start_date_dt.strftime("%Y-%m-%d")
            chunk_end_date = end_date_dt.strftime("%Y-%m-%d")

            # Debug output for the current chunk
            print(f"Fetching data for {symbol} from {chunk_start_date} to {chunk_end_date}")

            # Make the API request for the current chunk
            url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{chunk_start_date}/{chunk_end_date}"
            params = {
                "apiKey": self.api_key
            }
            response = requests.get(url, params=params)
            if response.status_code == 403:
                raise Exception(f"Error during data download: {response.status_code} {response.reason} for url: {response.url}")
            response.raise_for_status()
            data = response.json()

            # Convert the data to a DataFrame
            df = pd.DataFrame(data['results'])
            df['t'] = pd.to_datetime(df['t'], unit='ms')
            df.rename(columns={
                'o': 'Open',
                'h': 'High',
                'l': 'Low',
                'c': 'Close',
                'v': 'Volume',
                't': 'Date'
            }, inplace=True)
            df.set_index('Date', inplace=True)

            # Append the chunk DataFrame to the combined DataFrame
            combined_df = pd.concat([df, combined_df])

            # Update the end date for the next chunk
            end_date_dt = chunk_start_date_dt - timedelta(days=1)

        # Filter the combined data to ensure it matches the start and end dates
        combined_df = combined_df[(combined_df.index >= start_date) & (combined_df.index <= end_date)]
        return combined_df

    def save_to_csv(self, data, filename):
        data.to_csv(filename)

    def save_to_json(self, data, filename):
        data.to_json(filename, orient="records", date_format="iso")

class PolygonAdapter(DataAccessInterface):
    def __init__(self, api_key):
        self.adaptee = PolygonAdaptee(api_key)

    def fetch_data(self, symbol, start_date, end_date):
        return self.adaptee.fetch_data(symbol, start_date, end_date)

    def save_data(self, data, filename):
        self.adaptee.save_to_csv(data, filename)

    def save_data_as_json(self, data, filename):
        self.adaptee.save_to_json(data, filename)