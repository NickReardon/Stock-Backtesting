import pandas as pd
import matplotlib.pyplot as plt
from model import StrategyBase
import plot_utils as utils

strategy_name = "Bollinger Bands"

class BollingerBandsStrategy(StrategyBase):
    def execute_strategy(self, symbol: str, window: int, initial_balance: float):
        data = self.read_and_prepare_data(symbol)
        data['MA'] = data['Close'].rolling(window=window, min_periods=1).mean()
        data['STD'] = data['Close'].rolling(window=window, min_periods=1).std()
        data['Upper_Band'] = data['MA'] + (data['STD'] * 2)
        data['Lower_Band'] = data['MA'] - (data['STD'] * 2)
        self.save_indicator_data(data, ['MA', 'Upper_Band', 'Lower_Band'], 'bb_data.csv')
        balance, shares, trade_log, transactions = self.initialize_variables(initial_balance)
        balance, shares, trade_log, transactions = self.simulate_trades(
            data, symbol, balance, shares, trade_log, transactions,
            lambda data, i: data['Close'].iloc[i] < data['Lower_Band'].iloc[i] and data['Close'].iloc[i-1] >= data['Lower_Band'].iloc[i-1],
            lambda data, i: data['Close'].iloc[i] > data['Upper_Band'].iloc[i] and data['Close'].iloc[i-1] <= data['Upper_Band'].iloc[i-1]
        )
        total_gain_loss, total_return, annual_return = self.calculate_final_metrics(balance, initial_balance, data)
        self.add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return)
        self.save_trade_data(trade_log, transactions)

    def plot_strategy(self, fig: plt.Figure, data: pd.DataFrame, transactions: list, ticker: str):
        ax = fig.add_subplot(111)
        utils.plot_stock_price(ax, data, ticker)

        bb_data = pd.read_csv('bb_data.csv', index_col=0, parse_dates=True)
        print("Bollinger Bands Data Head:", bb_data.head())

        if bb_data.empty:
            print("No Bollinger Bands data to plot.")
            return

        ax.plot(bb_data.index, bb_data['MA'], label='Moving Average', color='orange')
        ax.plot(bb_data.index, bb_data['Upper_Band'], label='Upper Band', color='green')
        ax.plot(bb_data.index, bb_data['Lower_Band'], label='Lower Band', color='red')

        utils.plot_buy_sell_signals(ax, transactions)
        utils.customize_plot(ax, ticker, strategy_name)

# Ensure the strategy functions are accessible
def execute_strategy(symbol):
    strategy = BollingerBandsStrategy()
    strategy.execute_strategy(symbol, window=20, initial_balance=100000)

def plot_strategy(fig, data, transactions, ticker):
    strategy = BollingerBandsStrategy()
    strategy.plot_strategy(fig, data, transactions, ticker)