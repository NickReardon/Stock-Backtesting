import pandas as pd
from alpha_vantage_adapter import AlphaVantageAdapter
from yfinance_adapter import YFinanceAdapter

def compare_adapters(symbol, start_date, end_date):
    # Initialize adapters
    alpha_adapter = AlphaVantageAdapter()
    yfinance_adapter = YFinanceAdapter()

    # Fetch data using Alpha Vantage
    print("Fetching data using Alpha Vantage...")
    alpha_data = alpha_adapter.fetch_data(symbol, start_date, end_date)
    print("Alpha Vantage Data:")
    print(alpha_data)

    # Fetch data using yfinance
    print("\nFetching data using yfinance...")
    yfinance_data = yfinance_adapter.fetch_data(symbol, start_date, end_date)
    print("yfinance Data:")
    print(yfinance_data)

    # Compare the data
    print("\nComparing data...")
    comparison = pd.concat([alpha_data.set_index('Date'), yfinance_data.set_index('Date')], axis=1, keys=['Alpha Vantage', 'yfinance'])
    print(comparison)

if __name__ == "__main__":
    symbol = "FNGU"
    start_date = "2021-01-01"
    end_date = "2021-01-10"
    compare_adapters(symbol, start_date, end_date)