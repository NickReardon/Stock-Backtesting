import strategy as strat
import plot_utils as utils
import pandas as pd

strategy_name = "SMA Crossover"

def sma_crossover_strategy(symbol, short_window=40, long_window=100, initial_balance=100000):
    data = strat.read_and_prepare_data(symbol)
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    strat.save_indicator_data(data, ['Short_MA', 'Long_MA'], 'sma_data.csv')
    balance, shares, trade_log, transactions = strat.initialize_variables(initial_balance)
    balance, shares, trade_log, transactions = strat.simulate_trades(
        data, symbol, balance, shares, trade_log, transactions,
        lambda data, i: data['Short_MA'].iloc[i] > data['Long_MA'].iloc[i] and data['Short_MA'].iloc[i-1] <= data['Long_MA'].iloc[i-1],
        lambda data, i: data['Short_MA'].iloc[i] < data['Long_MA'].iloc[i] and data['Short_MA'].iloc[i-1] >= data['Long_MA'].iloc[i-1]
    )
    total_gain_loss, total_return, annual_return = strat.calculate_final_metrics(balance, initial_balance, data)
    strat.add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return)
    strat.save_trade_data(trade_log, transactions)

def plot_strategy(fig, data, transactions, ticker):
    ax = fig.add_subplot(111)
    utils.plot_stock_price(ax, data)
    
    sma_data = pd.read_csv('sma_data.csv', index_col=0, parse_dates=True)
    print("SMA Data Head:", sma_data.head())

    if sma_data.empty:
        print("No SMA data to plot.")
        return

    # Calculate the difference between Short_MA and Long_MA
    sma_diff = sma_data['Short_MA'] - sma_data['Long_MA']

    # Plot Short_MA in green where it is above Long_MA and red where it is below
    ax.plot(sma_data.index, sma_data['Long_MA'], label='Long MA', color='green')
    ax.fill_between(sma_data.index, sma_data['Short_MA'], sma_data['Long_MA'],
                    where=(sma_diff > 0), color='green', alpha=0.5, interpolate=True)
    ax.fill_between(sma_data.index, sma_data['Short_MA'], sma_data['Long_MA'],
                    where=(sma_diff <= 0), color='red', alpha=0.5, interpolate=True)
    ax.plot(sma_data.index, sma_data['Short_MA'], label='Short MA', color='red')

    utils.plot_buy_sell_signals(ax, transactions)
    utils.customize_plot(ax, ticker, strategy_name)