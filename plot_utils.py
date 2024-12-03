# plot_utils.py

import pandas as pd
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MaxNLocator

# Define variables for date format, axis font size, and number of ticks
DATE_FORMAT = '%m/%y'  # Default date format
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
X_AXIS_TICK_FONT_SIZE = 8  # Font size for x-axis ticks
NUMBER_OF_TICKS = 24       # Number of ticks on the x-axis

def plot_stock_price(ax, data):
    ax.plot(data.index, data['Close'], label='Close Price', color='black')

def plot_buy_sell_signals(ax, transactions):
    buy_signals = transactions[transactions['Action'] == 'Buy']
    sell_signals = transactions[transactions['Action'] == 'Sell']
    
    # Increase marker size and add edge color for better visibility
    ax.plot(buy_signals['Date'], buy_signals['Price'], '^', markersize=12, color='green', 
            markeredgecolor='black', markeredgewidth=1.5, lw=0, label='Buy Signal')
    ax.plot(sell_signals['Date'], sell_signals['Price'], 'v', markersize=12, color='red', 
            markeredgecolor='black', markeredgewidth=1.5, lw=0, label='Sell Signal')
    
def plot_stock_price(ax, data):
    ax.plot(data.index, data['Close'], label='Close Price', color='black')

def plot_buy_sell_signals(ax, transactions):
    buy_signals = transactions[transactions['Action'] == 'Buy']
    sell_signals = transactions[transactions['Action'] == 'Sell']
    
    # Increase marker size and add edge color for better visibility
    ax.plot(buy_signals['Date'], buy_signals['Price'], '^', markersize=7, color='green', 
            markeredgecolor='black', markeredgewidth=1, lw=0, label='Buy Signal')
    ax.plot(sell_signals['Date'], sell_signals['Price'], 'v', markersize=7, color='red', 
            markeredgecolor='black', markeredgewidth=1, lw=0, label='Sell Signal')
    
def customize_plot(ax, ticker, strategy_name):
    # Increase the number of ticks on the x-axis
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
    
    # Ensure a consistent number of ticks (e.g., 24 ticks)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))

    # Rotate the date labels and set font size
    ax.tick_params(axis='x', rotation=45, labelsize=X_AXIS_TICK_FONT_SIZE)

    # Add grid lines
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    
    # Set title and labels
    ax.set_title(f"{ticker} {strategy_name} Strategy Performance", fontsize=TITLE_FONT_SIZE)
    ax.set_xlabel("Date", fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel("Price", fontsize=AXIS_FONT_SIZE)
    
    # Add legend
    ax.legend()
    
    # Adjust the bottom margin
    ax.figure.subplots_adjust(bottom=0.17)