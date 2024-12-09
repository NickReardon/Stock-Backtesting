# plot_utils.py

import pandas as pd
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MaxNLocator

# Define variables for date format, axis font size, and number of ticks
DATE_FORMAT = '%m/%y'  # Default date format
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
X_AXIS_TICK_FONT_SIZE = 6  # Font size for x-axis ticks
NUMBER_OF_TICKS = 24       # Number of ticks on the x-axis

LEFT_MARGIN_SMALL = 0.075
LEFT_MARGIN_LARGE = 0.12
RIGHT_MARGIN_SMALL = 0.05
RIGHT_MARGIN_LARGE = 0.1
TOP_MARGIN_SMALL = 0.05
TOP_MARGIN_LARGE = 0.1
BOTTOM_MARGIN_LARGE = 0.2
BOTTOM_MARGIN_SMALL = 0.1

def plot_stock_price(ax, data):
    ax.plot(data.index, data['Close'], label='Close Price', color='black')

def plot_buy_sell_signals(ax, transactions):
    buy_signals = transactions[transactions['Action'] == 'Buy']
    sell_signals = transactions[transactions['Action'] == 'Sell']
    
    ax.plot(buy_signals['Date'], buy_signals['Price'], '^', markersize=7, color='green', 
            markeredgecolor='black', markeredgewidth=.5, lw=0, label='Buy Signal')
    ax.plot(sell_signals['Date'], sell_signals['Price'], 'v', markersize=7, color='red', 
            markeredgecolor='black', markeredgewidth=.5, lw=0, label='Sell Signal')

def customize_plot(ax, ticker, strategy_name):
    locator = AutoDateLocator(maxticks={
        'YEARLY': NUMBER_OF_TICKS,
        'MONTHLY': NUMBER_OF_TICKS,
        'DAILY': NUMBER_OF_TICKS,
        'HOURLY': NUMBER_OF_TICKS,
        'MINUTELY': NUMBER_OF_TICKS,
        'SECONDLY': NUMBER_OF_TICKS
    })
    formatter = DateFormatter(DATE_FORMAT)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))
    ax.tick_params(axis='x', rotation=45, labelsize=X_AXIS_TICK_FONT_SIZE)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlabel("Date", fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel("Price", fontsize=AXIS_FONT_SIZE)
    ax.legend()
    ax.figure.subplots_adjust(bottom=0.17)