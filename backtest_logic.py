from matplotlib.ticker import MaxNLocator
import pandas as pd
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import AutoDateLocator, DateFormatter
from plot_utils import plot_stock_price, plot_buy_sell_signals, DATE_FORMAT, AXIS_FONT_SIZE, TITLE_FONT_SIZE, X_AXIS_TICK_FONT_SIZE, NUMBER_OF_TICKS
from strategy import strategies

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

# region Backtest Methods
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
# endregion

# region Plotting Methods
def plot_strategy_performance(backtest_window, ticker, strategy_name):
    data, transactions = load_data(ticker)
    if data.empty or transactions.empty:
        print("No data to plot.")
        return

    fig, canvas = setup_canvas(backtest_window)
    adjust_margins(fig)

    # Get the plot function from the strategy
    plot_function = strategies[strategy_name]['plot']
    if plot_function:
        plot_function(fig, data, transactions, ticker)  # Pass data and transactions



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
# endregion