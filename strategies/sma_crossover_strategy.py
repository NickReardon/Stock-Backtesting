# sma_crossover_strategy.py
import pandas as pd
import matplotlib.pyplot as plt
from model import StrategyBase
import plot_utils as utils

strategy_name = "SMA Crossover"

class SMACrossoverStrategy(StrategyBase):
    def execute_strategy(self, symbol: str, short_window: int, long_window: int, initial_balance: float):
        
        print("Executing SMA Crossover Strategy")
        
        data = self.read_and_prepare_data(symbol)
        data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
        data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
        balance, shares, trade_log, transactions = self.initialize_variables(initial_balance)
        balance, shares, trade_log, transactions = self.simulate_trades(
            data, symbol, balance, shares, trade_log, transactions,
            lambda data, i: data['Short_MA'].iloc[i] > data['Long_MA'].iloc[i] and data['Short_MA'].iloc[i-1] <= data['Long_MA'].iloc[i-1],
            lambda data, i: data['Short_MA'].iloc[i] < data['Long_MA'].iloc[i] and data['Short_MA'].iloc[i-1] >= data['Long_MA'].iloc[i-1]
        )
        return self.make_result(trade_log, transactions, data[['Short_MA', 'Long_MA']], balance, initial_balance, data)

    def plot_strategy(self, fig: plt.Figure, data: pd.DataFrame, result, ticker: str):
        
        print("Plotting SMA Crossover Strategy")
        
        ax = fig.add_subplot(111)
        utils.plot_stock_price(ax, data, ticker)
        
        sma_data = result.indicators
        print("SMA Data Head:", sma_data.head())

        if sma_data.empty:
            print("No SMA data to plot.")
            return

        sma_diff = sma_data['Short_MA'] - sma_data['Long_MA']

        ax.plot(sma_data.index, sma_data['Long_MA'], label='Long MA', color='green')
        ax.fill_between(sma_data.index, sma_data['Short_MA'], sma_data['Long_MA'],
                        where=(sma_diff > 0), color='green', alpha=0.5, interpolate=True)
        ax.fill_between(sma_data.index, sma_data['Short_MA'], sma_data['Long_MA'],
                        where=(sma_diff <= 0), color='red', alpha=0.5, interpolate=True)
        ax.plot(sma_data.index, sma_data['Short_MA'], label='Short MA', color='red')

        utils.plot_buy_sell_signals(ax, result.transactions)
        utils.customize_plot(ax, ticker, strategy_name)

# Ensure the strategy functions are accessible
def execute_strategy(symbol):
    strategy = SMACrossoverStrategy()
    return strategy.execute_strategy(symbol, short_window=20, long_window=40, initial_balance=100000)

def plot_strategy(fig, data, result, ticker):
    strategy = SMACrossoverStrategy()
    strategy.plot_strategy(fig, data, result, ticker)