from matplotlib.ticker import MaxNLocator
import pandas as pd
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.pyplot as plt

# Define variables for date format, axis font size, and number of ticks
DATE_FORMAT = '%m/%y'  # Default date format
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
X_AXIS_TICK_FONT_SIZE = 8  # Font size for x-axis ticks
NUMBER_OF_TICKS = 24       # Number of ticks on the x-axis

# Define variables for margins and font sizes
LEFT_MARGIN_SMALL = 0.075
LEFT_MARGIN_LARGE = 0.12
RIGHT_MARGIN_SMALL = 0.05
RIGHT_MARGIN_LARGE = 0.1
TOP_MARGIN_SMALL = 0.05
TOP_MARGIN_LARGE = 0.1
BOTTOM_MARGIN_SMALL = 0.1
BOTTOM_MARGIN_LARGE = 0.2

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

def run_backtest_algorithm(symbol, strategy):
    # Run the selected strategy
    strategy(symbol)

    # Read the results log from the CSV file
    results_log = pd.read_csv('results.csv')

    return results_log

def load_backtest_data(backtest_window):
    # Load and display the backtest data in the backtest window
    print("Loading backtest data...")

    # Load the results CSV file
    df = pd.read_csv('results.csv')
    
    # Separate the last row as results
    df_data = df.iloc[:-1]
    df_results = df.iloc[-1:]

    # Display main data
    backtest_window.ui.backtestTable.setRowCount(len(df_data))
    backtest_window.ui.backtestTable.setColumnCount(len(df_data.columns))
    backtest_window.ui.backtestTable.setHorizontalHeaderLabels(df_data.columns)

    for i, row in df_data.iterrows():
        for j, value in enumerate(row):
            # Format date to dd/mm/yyyy
            if df_data.columns[j] == 'Date':
                value = pd.to_datetime(value).strftime('%d/%m/%Y')
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center-justify the text
            # Format dollar amounts to 2 decimal points with a dollar sign
            elif df_data.columns[j] in ['Price', 'Transaction Amount', 'Gain/Loss', 'Balance']:
                value = f"${float(value):.2f}"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Right-justify the text
            elif df_data.columns[j] == 'Shares':
                value = f"{int(value)}"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Right-justify the text
            else:
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Center-justify the text
            backtest_window.ui.backtestTable.setItem(i, j, item)

    # Resize columns to fit the content
    backtest_window.ui.backtestTable.resizeColumnsToContents()

    # Adjust the size of the table to fit its contents
    backtest_window.ui.backtestTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    backtest_window.ui.backtestTable.setMinimumSize(backtest_window.ui.backtestTable.sizeHint())

    # Display results using QStandardItemModel
    model = QStandardItemModel(1, 4)  # 4 columns for the results table
    model.setHorizontalHeaderLabels(["Total Gain/Loss", "Balance", "Total Return", "Annual Return"])

    for j, value in enumerate(df_results.iloc[0]):
        header_item = model.horizontalHeaderItem(j)
        if header_item:
            if header_item.text() in ["Total Gain/Loss", "Balance"]:
                value = f"${float(value):.2f}"
            elif header_item.text() in ["Total Return", "Annual Return"]:
                value = f"{float(value):.2f}%"
        item = QStandardItem(str(value))
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Right-justify the text
        model.setItem(0, j, item)

    backtest_window.ui.resultsTable.setModel(model)
    backtest_window.ui.resultsTable.resizeColumnsToContents()

    # Adjust the size of the table to fit its contents
    backtest_window.ui.resultsTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    backtest_window.ui.resultsTable.setMinimumSize(backtest_window.ui.resultsTable.sizeHint())

    # Remove any columns after the 4th in the backtest table
    while backtest_window.ui.resultsTable.model().columnCount() > 4:
        backtest_window.ui.resultsTable.model().removeColumn(4)

def plot_strategy_performance(backtest_window, ticker, strategy_name):
    data, transactions = load_data(ticker)
    if data.empty or transactions.empty:
        print("No data to plot.")
        return

    fig, canvas = setup_canvas(backtest_window)
    adjust_margins(fig)

    if strategy_name == "MACD":
        plot_macd_strategy(fig, data, transactions, ticker)
    else:
        ax = fig.add_subplot(111)
        plot_stock_price(ax, data)

        if strategy_name == "SMA Crossover":
            plot_sma_strategy(ax)
        elif strategy_name == "Bollinger Bands":
            plot_bollinger_bands_strategy(ax)

        plot_buy_sell_signals(ax, transactions)
        customize_plot(ax, ticker, strategy_name)

    canvas.draw()

def load_data(ticker):
    data = pd.read_json('all_symbols_data.json', convert_dates=True)
    data = data[data['Symbol'] == ticker]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    transactions = pd.read_csv('transactions.csv', parse_dates=['Date'])

    print("Filtered Data Head:", data.head())
    print("Transactions Head:", transactions.head())

    return data, transactions

def setup_canvas(backtest_window):
    fig = Figure(figsize=(10, 8), dpi=100)
    canvas = FigureCanvas(fig)
    layout = QVBoxLayout(backtest_window.ui.backtestPlot)
    layout.addWidget(canvas)
    return fig, canvas

def adjust_margins(fig):
    # Adjust margins based on the current size of the canvas
    width, height = fig.get_size_inches() * fig.dpi
    left_margin = LEFT_MARGIN_LARGE if width < 800 else LEFT_MARGIN_SMALL
    right_margin = RIGHT_MARGIN_LARGE if width < 800 else RIGHT_MARGIN_SMALL
    top_margin = TOP_MARGIN_LARGE if height < 600 else TOP_MARGIN_SMALL
    bottom_margin = BOTTOM_MARGIN_LARGE if height < 600 else BOTTOM_MARGIN_SMALL
    fig.subplots_adjust(left=left_margin, bottom=bottom_margin, right=1-right_margin, top=1-top_margin)


    
def plot_macd_strategy(fig, data, transactions, ticker):
    macd_data = pd.read_csv('macd_data.csv', index_col=0, parse_dates=True)
    print("MACD Data Head:", macd_data.head())

    if macd_data.empty:
        print("No MACD data to plot.")
        return

    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex=ax1)

    plot_stock_price(ax1, data)
    plot_buy_sell_signals(ax1, transactions)

    ax1.set_title(f"{ticker} MACD Strategy Performance", fontsize=TITLE_FONT_SIZE)
    ax1.set_ylabel("Price", fontsize=AXIS_FONT_SIZE)
    ax1.legend()
    ax1.grid(True)

    # Calculate the difference between MACD and Signal Line
    macd_diff = macd_data['MACD'] - macd_data['Signal_Line']

    # Plot MACD in green where it is above the signal line and red where it is below
    ax2.plot(macd_data.index, macd_data['Signal_Line'], label='Signal Line', color='brown')
    ax2.fill_between(macd_data.index, macd_data['MACD'], macd_data['Signal_Line'],
                     where=(macd_diff > 0), color='green', alpha=0.5, interpolate=True)
    ax2.fill_between(macd_data.index, macd_data['MACD'], macd_data['Signal_Line'],
                     where=(macd_diff <= 0), color='red', alpha=0.5, interpolate=True)
    ax2.plot(macd_data.index, macd_data['MACD'], label='MACD', color='purple')

    ax2.set_ylabel("MACD", fontsize=AXIS_FONT_SIZE)
    ax2.legend()
    ax2.grid(True)

    locator = AutoDateLocator()
    formatter = DateFormatter(DATE_FORMAT)

    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
   
    # Ensure a consistent number of ticks (e.g., 24 ticks)
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))

    # Rotate the date labels and set font size
    ax1.tick_params(axis='x', rotation=45, labelsize=X_AXIS_TICK_FONT_SIZE)

    # Add grid lines
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax2.xaxis.set_major_locator(locator)
    ax2.xaxis.set_major_formatter(formatter)
   
    # Ensure a consistent number of ticks (e.g., 24 ticks)
    ax2.xaxis.set_major_locator(MaxNLocator(nbins=NUMBER_OF_TICKS))

    # Rotate the date labels and set font size
    ax2.tick_params(axis='x', rotation=45, labelsize=X_AXIS_TICK_FONT_SIZE)

    # Add grid lines
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

    fig.subplots_adjust(bottom=0.17)

def plot_sma_strategy(ax):
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

def plot_bollinger_bands_strategy(ax):
    bb_data = pd.read_csv('bb_data.csv', index_col=0, parse_dates=True)
    print("Bollinger Bands Data Head:", bb_data.head())

    if bb_data.empty:
        print("No Bollinger Bands data to plot.")
        return

    ax.plot(bb_data.index, bb_data['MA'], label='Moving Average', color='orange')
    ax.plot(bb_data.index, bb_data['Upper_Band'], label='Upper Band', color='green')
    ax.plot(bb_data.index, bb_data['Lower_Band'], label='Lower Band', color='red')

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