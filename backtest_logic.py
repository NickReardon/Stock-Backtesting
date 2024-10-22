import pandas as pd
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import AutoDateLocator, DateFormatter

DATE_FORMAT = '%m/%y'  # Default date format
AXIS_FONT_SIZE = 10
TITLE_FONT_SIZE = 12

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

def run_backtest_algorithm(symbol, strategy):
    # Read data from the combined JSON file for all symbols
    all_data = pd.read_json("all_symbols_data.json", orient="records")
    
    # Filter data for the selected symbol
    data = all_data[all_data['Symbol'] == symbol]
    data.loc[:, 'Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Run the selected strategy on the filtered data
    data = strategy(data, symbol)

    # Read the results log from the CSV file
    results_log = pd.read_csv('results.csv')

    return data, results_log

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

def plot_strategy_performance(backtest_window, data, results_log, ticker):
    if data is None or data.empty:
        print("No data to plot.")
        return

    canvas = MplCanvas(backtest_window, width=5, height=4, dpi=100)
    layout = QVBoxLayout(backtest_window.ui.backtestPlot)
    layout.addWidget(canvas)

    canvas.axes.clear()

    # Plot the stock price
    canvas.axes.plot(data.index, data['Close'], label='Close Price', color='blue')

    # Plot the short and long moving averages
    sma_data = pd.read_csv('sma_data.csv', index_col=0, parse_dates=True)
    canvas.axes.plot(sma_data.index, sma_data['Short_MA'], label='Short MA', color='red')
    canvas.axes.plot(sma_data.index, sma_data['Long_MA'], label='Long MA', color='green')

    # Plot buy and sell signals
    transactions = pd.read_csv('transactions.csv', parse_dates=['Date'])
    buy_signals = transactions[transactions['Action'] == 'Buy']
    sell_signals = transactions[transactions['Action'] == 'Sell']
    canvas.axes.plot(buy_signals['Date'], buy_signals['Price'], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    canvas.axes.plot(sell_signals['Date'], sell_signals['Price'], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

    # Customize the x-axis
    locator = AutoDateLocator()
    formatter = DateFormatter(DATE_FORMAT)
    canvas.axes.xaxis.set_major_locator(locator)
    canvas.axes.xaxis.set_major_formatter(formatter)

    # Rotate the date labels
    canvas.axes.tick_params(axis='x', rotation=45, labelsize=AXIS_FONT_SIZE)

    # Add grid lines
    canvas.axes.grid(True)

    # Set title and labels
    canvas.axes.set_title(f"{ticker} SMA Cross-over Strategy Performance", fontsize=TITLE_FONT_SIZE)
    canvas.axes.set_xlabel("Date", fontsize=AXIS_FONT_SIZE)
    canvas.axes.set_ylabel("Price", fontsize=AXIS_FONT_SIZE)

    # Add legend
    canvas.axes.legend()

    canvas.draw()