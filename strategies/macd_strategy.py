# macd_strategy.py
import pandas as pd
import matplotlib.pyplot as plt
from strategy import StrategyBase
import plot_utils as utils
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MaxNLocator

strategy_name = "MACD"

class MACDStrategy(StrategyBase):
    def execute_strategy(self, symbol: str, initial_balance: float):
        data = self.read_and_prepare_data(symbol)
        short_ema = data['Close'].ewm(span=12, adjust=False).mean()
        long_ema = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = short_ema - long_ema
        data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
        self.save_indicator_data(data, ['MACD', 'Signal_Line'], 'macd_data.csv')
        balance, shares, trade_log, transactions = self.initialize_variables(initial_balance)
        balance, shares, trade_log, transactions = self.simulate_trades(
            data, symbol, balance, shares, trade_log, transactions,
            lambda data, i: data['MACD'].iloc[i] > data['Signal_Line'].iloc[i] and data['MACD'].iloc[i-1] <= data['Signal_Line'].iloc[i-1],
            lambda data, i: data['MACD'].iloc[i] < data['Signal_Line'].iloc[i] and data['MACD'].iloc[i-1] >= data['Signal_Line'].iloc[i-1]
        )
        total_gain_loss, total_return, annual_return = self.calculate_final_metrics(balance, initial_balance, data)
        self.add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return)
        self.save_trade_data(trade_log, transactions)

    def plot_strategy(self, fig: plt.Figure, data: pd.DataFrame, transactions: list, ticker: str):
        macd_data = pd.read_csv('macd_data.csv', index_col=0, parse_dates=True)
        print("MACD Data Head:", macd_data.head())
        print("MACD Data Tail:", macd_data.tail())

        if macd_data.empty:
            print("No MACD data to plot.")
            return

        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212, sharex=ax1)

        utils.plot_stock_price(ax1, data, ticker)
        utils.plot_buy_sell_signals(ax1, transactions)

        ax1.set_title(f"{ticker} MACD Strategy Performance", fontsize=utils.TITLE_FONT_SIZE)
        ax1.set_ylabel("Price", fontsize=utils.AXIS_FONT_SIZE)
        ax1.legend()
        ax1.grid(True)

        # Calculate the difference between MACD and Signal Line
        macd_diff = macd_data['MACD'] - macd_data['Signal_Line']
        print("MACD Diff Head:", macd_diff.head())
        print("MACD Diff Tail:", macd_diff.tail())

        # Plot MACD in green where it is above the signal line and red where it is below
        ax2.plot(macd_data.index, macd_data['Signal_Line'], label='Signal Line', color='brown')
        ax2.fill_between(macd_data.index, macd_data['MACD'], macd_data['Signal_Line'],
                         where=(macd_diff > 0), color='green', alpha=0.5, interpolate=True)
        ax2.fill_between(macd_data.index, macd_data['MACD'], macd_data['Signal_Line'],
                         where=(macd_diff <= 0), color='red', alpha=0.5, interpolate=True)
        ax2.plot(macd_data.index, macd_data['MACD'], label='MACD', color='purple')

        ax2.set_ylabel("MACD", fontsize=utils.AXIS_FONT_SIZE)
        ax2.legend()
        ax2.grid(True)

        locator = AutoDateLocator()
        formatter = DateFormatter(utils.DATE_FORMAT)

        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(formatter)
        ax2.xaxis.set_major_locator(locator)
        ax2.xaxis.set_major_formatter(formatter)

        # Ensure a consistent number of ticks (e.g., 24 ticks)
        ax1.xaxis.set_major_locator(MaxNLocator(nbins=utils.NUMBER_OF_TICKS))
        ax1.tick_params(axis='x', rotation=45, labelsize=utils.X_AXIS_TICK_FONT_SIZE)
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

        ax2.xaxis.set_major_locator(MaxNLocator(nbins=utils.NUMBER_OF_TICKS))
        ax2.tick_params(axis='x', rotation=45, labelsize=utils.X_AXIS_TICK_FONT_SIZE)
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

        fig.subplots_adjust(bottom=0.17)

# Ensure the strategy functions are accessible
def execute_strategy(symbol):
    strategy = MACDStrategy()
    strategy.execute_strategy(symbol, initial_balance=100000)

def plot_strategy(fig, data, transactions, ticker):
    strategy = MACDStrategy()
    strategy.plot_strategy(fig, data, transactions, ticker)