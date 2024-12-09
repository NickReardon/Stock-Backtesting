# strategy.py
from abc import ABC, abstractmethod
import yfinance as yf
import pandas as pd
from PySide6.QtCore import QThread, Signal
import matplotlib.pyplot as plt
import os
import importlib
from decimal import Decimal, getcontext

class DownloadThread(QThread):
    download_complete = Signal()

    def __init__(self, symbols, start_date, end_date, data_access, parent=None):
        super().__init__(parent)
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.data_access = data_access

    def run(self):
        all_data = []
        try:
            for ticker in self.symbols:
                print(f"Fetching data for {ticker}...")
                data = self.data_access.fetch_data(ticker, self.start_date, self.end_date)
                data_to_save = data[['Open', 'High', 'Low', 'Close', 'Volume']]
                data_to_save.reset_index(inplace=True)
                data_to_save['Date'] = data_to_save['Date'].dt.strftime('%Y-%m-%d')
                data_to_save['Symbol'] = ticker
                all_data.append(data_to_save)
                print(f"Data for {ticker} fetched and processed.")

            combined_data = pd.concat(all_data, ignore_index=True)
            print("Combined data")

            self.data_access.save_data_as_json(combined_data, "all_symbols_data.json")
            print("Data saved to all_symbols_data.json")

            self.download_complete.emit()
        except Exception as e:
            print(f"Error during data download: {e}")
            

# Set the precision for Decimal
getcontext().prec = 28

class StrategyBase(ABC):
    def read_and_prepare_data(self, symbol):
        data = pd.read_json('all_symbols_data.json')
        data = data[data['Symbol'] == symbol]
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        return data

    def save_indicator_data(self, data, columns, filename):
        indicator_data = data[columns]
        indicator_data.to_csv(filename)

    def initialize_variables(self, initial_balance):
        balance = Decimal(initial_balance)
        shares = Decimal(0)
        trade_log = []
        transactions = []
        return balance, shares, trade_log, transactions

    def simulate_trades(self, data, symbol, balance, shares, trade_log, transactions, buy_condition, sell_condition):
        for i in range(1, len(data)):
            if buy_condition(data, i):
                balance, shares = self.buy(data, i, symbol, balance, shares, trade_log, transactions)
            elif sell_condition(data, i):
                balance, shares = self.sell(data, i, symbol, balance, shares, trade_log, transactions)
        balance, shares = self.sell(data, len(data) - 1, symbol, balance, shares, trade_log, transactions)
        return balance, shares, trade_log, transactions

    def calculate_final_metrics(self, balance, initial_balance, data):
        total_gain_loss = balance - Decimal(initial_balance)
        total_return = (balance / Decimal(initial_balance) - 1) * 100
        annual_return = Decimal(float(total_return) / (len(data) / 252))  # Assuming 252 trading days in a year
        return total_gain_loss, total_return, annual_return

    def add_summary_row(self, trade_log, total_gain_loss, balance, total_return, annual_return):
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

    def save_trade_data(self, trade_log, transactions):
        trade_log_df = pd.DataFrame(trade_log)
        trade_log_df.to_csv('results.csv', index=False)

        transactions_df = pd.DataFrame(transactions)
        transactions_df.to_csv('transactions.csv', index=False)

    def buy(self, data, i, symbol, balance, shares, trade_log, transactions):
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

    def sell(self, data, i, symbol, balance, shares, trade_log, transactions):
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

    @abstractmethod
    def execute_strategy(self, symbol: str, short_window: int, long_window: int, initial_balance: float):
        pass

    @abstractmethod
    def plot_strategy(self, fig: plt.Figure, data: pd.DataFrame, transactions: list, ticker: str):
        pass


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
                'strategy': getattr(module, 'execute_strategy', None),
                'plot': getattr(module, 'plot_strategy', None)
            }
    return strategies

strategies = load_strategies()