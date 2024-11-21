# strategy.py

import yfinance as yf
import pandas as pd
from PySide6.QtCore import QThread, Signal
import os
import importlib
from decimal import Decimal, getcontext

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



# Set the precision for Decimal
getcontext().prec = 28

# Universal Utility Functions
def calculate_final_metrics(balance, initial_balance, data):
    total_gain_loss = balance - Decimal(initial_balance)
    total_return = (balance / Decimal(initial_balance) - 1) * 100
    annual_return = Decimal(float(total_return) / (len(data) / 252))  # Assuming 252 trading days in a year
    return total_gain_loss, total_return, annual_return

def add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return):
    trade_log.append({
        'Date': f"{total_gain_loss:.2f}",
        'Symbol': f"{balance:.2f}",
        'Action': f"{total_return:.2f}",
        'Price': f"{annual_return:.2f}",
        'Shares': '',
        'Transaction Amount': '',
        'Gain/Loss': '',
        'Balance': ''
    })

def save_trade_data(trade_log, transactions):
    trade_log_df = pd.DataFrame(trade_log)
    trade_log_df.to_csv('results.csv', index=False)

    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv('transactions.csv', index=False)

# Universal Trading Functions
def buy(data, i, symbol, balance, shares, trade_log, transactions):
    shares_to_buy = balance // Decimal(data['Close'].iloc[i])
    if shares_to_buy > 0:
        transaction_amount = shares_to_buy * Decimal(data['Close'].iloc[i])
        balance -= transaction_amount
        shares += shares_to_buy
        trade_log.append({
            'Date': data.index[i],
            'Symbol': symbol,
            'Action': 'Buy',
            'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
            'Shares': f"{shares_to_buy:.2f}",
            'Transaction Amount': f"{transaction_amount:.2f}",
            'Gain/Loss': '0.00',
            'Balance': f"{balance:.2f}"
        })
        transactions.append({
            'Date': data.index[i],
            'Action': 'Buy',
            'Price': data['Close'].iloc[i]
        })
    return balance, shares

def sell(data, i, symbol, balance, shares, trade_log, transactions):
    if shares > 0:
        transaction_amount = shares * Decimal(data['Close'].iloc[i])
        gain_loss = transaction_amount - (shares * Decimal(data['Close'].iloc[i-1]))
        balance += transaction_amount
        trade_log.append({
            'Date': data.index[i],
            'Symbol': symbol,
            'Action': 'Sell',
            'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
            'Shares': f"{shares:.2f}",
            'Transaction Amount': f"{transaction_amount:.2f}",
            'Gain/Loss': f"{gain_loss:.2f}",
            'Balance': f"{balance:.2f}"
        })
        transactions.append({
            'Date': data.index[i],
            'Action': 'Sell',
            'Price': data['Close'].iloc[i]
        })
        shares = Decimal(0)
    return balance, shares

# Universal Helper Functions
def read_and_prepare_data(symbol):
    data = pd.read_json('all_symbols_data.json')
    data = data[data['Symbol'] == symbol]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data

def save_indicator_data(data, columns, filename):
    indicator_data = data[columns]
    indicator_data.to_csv(filename)

def initialize_variables(initial_balance):
    balance = Decimal(initial_balance)
    shares = Decimal(0)
    trade_log = []
    transactions = []
    return balance, shares, trade_log, transactions

def simulate_trades(data, symbol, balance, shares, trade_log, transactions, buy_condition, sell_condition):
    for i in range(1, len(data)):
        if buy_condition(data, i):
            balance, shares = buy(data, i, symbol, balance, shares, trade_log, transactions)
        elif sell_condition(data, i):
            balance, shares = sell(data, i, symbol, balance, shares, trade_log, transactions)
    balance, shares = sell(data, len(data) - 1, symbol, balance, shares, trade_log, transactions)
    return balance, shares, trade_log, transactions

# Dynamically load strategies from the strategies directory
def load_strategies():
    strategies = {}
    strategy_dir = os.path.join(os.path.dirname(__file__), 'strategies')
    for filename in os.listdir(strategy_dir):
        if filename.endswith('_strategy.py'):
            module_name = filename[:-3]
            module = importlib.import_module(f'strategies.{module_name}')
            strategy_function_name = module_name  # Correctly set the function name
            strategy_name = getattr(module, 'strategy_name', module_name.replace('_', ' ').title().replace('Strategy', '').strip())
            strategies[strategy_name] = {
                'strategy': getattr(module, strategy_function_name),
                'plot': getattr(module, 'plot_strategy', None)
            }
    return strategies

# Dictionary of strategies
strategies = load_strategies()