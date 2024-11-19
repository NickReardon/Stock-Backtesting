import strategy as strat
import plot_utils as utils
import pandas as pd
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MaxNLocator

strategy_name = "Bollinger Bands"

def bollinger_bands_strategy(symbol, window=20, initial_balance=100000):
    data = strat.read_and_prepare_data(symbol)
    data['MA'] = data['Close'].rolling(window=window, min_periods=1).mean()
    data['STD'] = data['Close'].rolling(window=window, min_periods=1).std()
    data['Upper_Band'] = data['MA'] + (data['STD'] * 2)
    data['Lower_Band'] = data['MA'] - (data['STD'] * 2)
    strat.save_indicator_data(data, ['MA', 'Upper_Band', 'Lower_Band'], 'bb_data.csv')
    balance, shares, trade_log, transactions = strat.initialize_variables(initial_balance)
    balance, shares, trade_log, transactions = strat.simulate_trades(
        data, symbol, balance, shares, trade_log, transactions,
        lambda data, i: data['Close'].iloc[i] < data['Lower_Band'].iloc[i] and data['Close'].iloc[i-1] >= data['Lower_Band'].iloc[i-1],
        lambda data, i: data['Close'].iloc[i] > data['Upper_Band'].iloc[i] and data['Close'].iloc[i-1] <= data['Upper_Band'].iloc[i-1]
    )
    total_gain_loss, total_return, annual_return = strat.calculate_final_metrics(balance, initial_balance, data)
    strat.add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return)
    strat.save_trade_data(trade_log, transactions)

def plot_strategy(fig, data, transactions, ticker):
    ax = fig.add_subplot(111)
    utils.plot_stock_price(ax, data)

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