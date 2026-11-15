# plot_utils.py
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

# Define variables for date format, axis font size, and number of ticks
DATE_FORMAT = '%m/%y'  # Default date format
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
X_AXIS_TICK_FONT_SIZE = 6  # Font size for x-axis ticks on strategy plots
MAIN_X_AXIS_TICK_FONT_SIZE = 8  # Font size for x-axis ticks on the main window plot
NUMBER_OF_TICKS = 24       # Number of ticks on the x-axis

LEFT_MARGIN_SMALL = 0.075
LEFT_MARGIN_LARGE = 0.12
RIGHT_MARGIN_SMALL = 0.05
RIGHT_MARGIN_LARGE = 0.1
TOP_MARGIN_SMALL = 0.05
TOP_MARGIN_LARGE = 0.1
BOTTOM_MARGIN_LARGE = 0.2
BOTTOM_MARGIN_SMALL = 0.1

def plot_stock_price(ax, data, ticker):
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.set_title(f"{ticker} Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()

def plot_buy_sell_signals(ax, transactions):
    buy_signals = transactions[transactions['Action'] == 'Buy']
    sell_signals = transactions[transactions['Action'] == 'Sell']
    
    ax.plot(buy_signals['Date'], buy_signals['Price'], '^', markersize=7, color='green', 
            markeredgecolor='black', markeredgewidth=.5, lw=0, label='Buy Signal')
    ax.plot(sell_signals['Date'], sell_signals['Price'], 'v', markersize=7, color='red', 
            markeredgecolor='black', markeredgewidth=.5, lw=0, label='Sell Signal')

def format_date_axis(ax, x_tick_font_size=X_AXIS_TICK_FONT_SIZE):
    ax.xaxis.set_major_formatter(DateFormatter(DATE_FORMAT))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))
    ax.tick_params(axis='x', rotation=45, labelsize=x_tick_font_size)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

def customize_plot(ax, ticker, strategy_name, legend=True, x_tick_font_size=X_AXIS_TICK_FONT_SIZE):
    format_date_axis(ax, x_tick_font_size)
    ax.set_xlabel("Date", fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel("Price", fontsize=AXIS_FONT_SIZE)
    if legend:
        ax.legend()
    ax.figure.subplots_adjust(bottom=0.17)

def adjust_margins(fig):
    """Adjust margins based on the current size of the figure."""
    width, height = fig.get_size_inches() * fig.dpi
    left_margin = LEFT_MARGIN_LARGE if width < 800 else LEFT_MARGIN_SMALL
    right_margin = RIGHT_MARGIN_LARGE if width < 800 else RIGHT_MARGIN_SMALL
    top_margin = TOP_MARGIN_LARGE if height < 600 else TOP_MARGIN_SMALL
    bottom_margin = BOTTOM_MARGIN_LARGE if height < 600 else BOTTOM_MARGIN_SMALL
    fig.subplots_adjust(left=left_margin, bottom=bottom_margin, right=1-right_margin, top=1-top_margin)
