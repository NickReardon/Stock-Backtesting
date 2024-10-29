import pandas as pd
from decimal import Decimal, getcontext

# Set the precision for Decimal
getcontext().prec = 28

def calculate_final_metrics(balance, initial_balance, data):
    total_gain_loss = balance - Decimal(initial_balance)
    total_return = (balance / Decimal(initial_balance) - 1) * 100
    annual_return = Decimal(float(total_return) / (len(data) / 252))  # Assuming 252 trading days in a year
    return total_gain_loss, total_return, annual_return

def add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return):
    trade_log.append({
        'Date': f"{total_gain_loss:.2f}",
        'Symbol': f"{balance:.2f}",
        'Action': f"{total_return:.2f}",
        'Price': f"{annual_return:.2f}",
        'Shares': '',
        'Transaction Amount': '',
        'Gain/Loss': '',
        'Balance': ''
    })

def save_trade_data(trade_log, transactions):
    # Save trade log to results.csv
    trade_log_df = pd.DataFrame(trade_log)
    trade_log_df.to_csv('results.csv', index=False)

    # Save transactions to transactions.csv
    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv('transactions.csv', index=False)

def sma_crossover_strategy(symbol, short_window=40, long_window=100, initial_balance=100000):
    # Read data from JSON file
    data = pd.read_json('all_symbols_data.json')
    data = data[data['Symbol'] == symbol]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Calculate short and long moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    # Save the SMA data for plotting
    sma_data = data[['Short_MA', 'Long_MA']]
    sma_data.to_csv('sma_data.csv')

    # Initialize variables
    balance = Decimal(initial_balance)
    shares = Decimal(0)
    trade_log = []
    transactions = []

    # Iterate over the data to simulate trades
    for i in range(1, len(data)):
        if data['Short_MA'].iloc[i] > data['Long_MA'].iloc[i] and data['Short_MA'].iloc[i-1] <= data['Long_MA'].iloc[i-1]:
            # Buy signal
            shares_to_buy = balance // Decimal(data['Close'].iloc[i])
            if shares_to_buy > 0:
                transaction_amount = shares_to_buy * Decimal(data['Close'].iloc[i])
                balance -= transaction_amount
                shares += shares_to_buy
                trade_log.append({
                    'Date': data.index[i],
                    'Symbol': symbol,
                    'Action': 'Buy',
                    'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
                    'Shares': f"{shares_to_buy:.2f}",
                    'Transaction Amount': f"{transaction_amount:.2f}",
                    'Gain/Loss': '0.00',
                    'Balance': f"{balance:.2f}"
                })
                transactions.append({
                    'Date': data.index[i],
                    'Action': 'Buy',
                    'Price': data['Close'].iloc[i]
                })
        elif data['Short_MA'].iloc[i] < data['Long_MA'].iloc[i] and data['Short_MA'].iloc[i-1] >= data['Long_MA'].iloc[i-1]:
            # Sell signal
            if shares > 0:
                transaction_amount = shares * Decimal(data['Close'].iloc[i])
                gain_loss = transaction_amount - (shares * Decimal(data['Close'].iloc[i-1]))
                balance += transaction_amount
                trade_log.append({
                    'Date': data.index[i],
                    'Symbol': symbol,
                    'Action': 'Sell',
                    'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
                    'Shares': f"{shares:.2f}",
                    'Transaction Amount': f"{transaction_amount:.2f}",
                    'Gain/Loss': f"{gain_loss:.2f}",
                    'Balance': f"{balance:.2f}"
                })
                transactions.append({
                    'Date': data.index[i],
                    'Action': 'Sell',
                    'Price': data['Close'].iloc[i]
                })
                shares = Decimal(0)

    # Calculate final metrics
    total_gain_loss, total_return, annual_return = calculate_final_metrics(balance, initial_balance, data)

    # Add summary row
    add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return)

    # Save trade log and transactions
    save_trade_data(trade_log, transactions)

def bollinger_bands_strategy(symbol, window=20, initial_balance=100000):
    # Read data from JSON file
    data = pd.read_json('all_symbols_data.json')
    data = data[data['Symbol'] == symbol]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Calculate Bollinger Bands
    data['MA'] = data['Close'].rolling(window=window, min_periods=1).mean()
    data['STD'] = data['Close'].rolling(window=window, min_periods=1).std()
    data['Upper_Band'] = data['MA'] + (data['STD'] * 2)
    data['Lower_Band'] = data['MA'] - (data['STD'] * 2)

    # Save the Bollinger Bands data for plotting
    bb_data = data[['MA', 'Upper_Band', 'Lower_Band']]
    bb_data.to_csv('bb_data.csv')

    # Initialize variables
    balance = Decimal(initial_balance)
    shares = Decimal(0)
    trade_log = []
    transactions = []

    # Iterate over the data to simulate trades
    for i in range(1, len(data)):
        if data['Close'].iloc[i] < data['Lower_Band'].iloc[i] and data['Close'].iloc[i-1] >= data['Lower_Band'].iloc[i-1]:
            # Buy signal
            shares_to_buy = balance // Decimal(data['Close'].iloc[i])
            if shares_to_buy > 0:
                transaction_amount = shares_to_buy * Decimal(data['Close'].iloc[i])
                balance -= transaction_amount
                shares += shares_to_buy
                trade_log.append({
                    'Date': data.index[i],
                    'Symbol': symbol,
                    'Action': 'Buy',
                    'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
                    'Shares': f"{shares_to_buy:.2f}",
                    'Transaction Amount': f"{transaction_amount:.2f}",
                    'Gain/Loss': '0.00',
                    'Balance': f"{balance:.2f}"
                })
                transactions.append({
                    'Date': data.index[i],
                    'Action': 'Buy',
                    'Price': data['Close'].iloc[i]
                })
        elif data['Close'].iloc[i] > data['Upper_Band'].iloc[i] and data['Close'].iloc[i-1] <= data['Upper_Band'].iloc[i-1]:
            # Sell signal
            if shares > 0:
                transaction_amount = shares * Decimal(data['Close'].iloc[i])
                gain_loss = transaction_amount - (shares * Decimal(data['Close'].iloc[i-1]))
                balance += transaction_amount
                trade_log.append({
                    'Date': data.index[i],
                    'Symbol': symbol,
                    'Action': 'Sell',
                    'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
                    'Shares': f"{shares:.2f}",
                    'Transaction Amount': f"{transaction_amount:.2f}",
                    'Gain/Loss': f"{gain_loss:.2f}",
                    'Balance': f"{balance:.2f}"
                })
                transactions.append({
                    'Date': data.index[i],
                    'Action': 'Sell',
                    'Price': data['Close'].iloc[i]
                })
                shares = Decimal(0)

    # Calculate final metrics
    total_gain_loss, total_return, annual_return = calculate_final_metrics(balance, initial_balance, data)

    # Add summary row
    add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return)

    # Save trade log and transactions
    save_trade_data(trade_log, transactions)

def macd_strategy(symbol, initial_balance=100000):
    # Read data from JSON file
    data = pd.read_json('all_symbols_data.json')
    data = data[data['Symbol'] == symbol]
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Calculate MACD and Signal Line
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = short_ema - long_ema
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # Save the MACD data for plotting
    macd_data = data[['MACD', 'Signal_Line']]
    macd_data.to_csv('macd_data.csv')

    # Initialize variables
    balance = Decimal(initial_balance)
    shares = Decimal(0)
    trade_log = []
    transactions = []

    # Iterate over the data to simulate trades
    for i in range(1, len(data)):
        if data['MACD'].iloc[i] > data['Signal_Line'].iloc[i] and data['MACD'].iloc[i-1] <= data['Signal_Line'].iloc[i-1]:
            # Buy signal
            shares_to_buy = balance // Decimal(data['Close'].iloc[i])
            if shares_to_buy > 0:
                transaction_amount = shares_to_buy * Decimal(data['Close'].iloc[i])
                balance -= transaction_amount
                shares += shares_to_buy
                trade_log.append({
                    'Date': data.index[i],
                    'Symbol': symbol,
                    'Action': 'Buy',
                    'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
                    'Shares': f"{shares_to_buy:.2f}",
                    'Transaction Amount': f"{transaction_amount:.2f}",
                    'Gain/Loss': '0.00',
                    'Balance': f"{balance:.2f}"
                })
                transactions.append({
                    'Date': data.index[i],
                    'Action': 'Buy',
                    'Price': data['Close'].iloc[i]
                })
        elif data['MACD'].iloc[i] < data['Signal_Line'].iloc[i] and data['MACD'].iloc[i-1] >= data['Signal_Line'].iloc[i-1]:
            # Sell signal
            if shares > 0:
                transaction_amount = shares * Decimal(data['Close'].iloc[i])
                gain_loss = transaction_amount - (shares * Decimal(data['Close'].iloc[i-1]))
                balance += transaction_amount
                trade_log.append({
                    'Date': data.index[i],
                    'Symbol': symbol,
                    'Action': 'Sell',
                    'Price': f"{Decimal(data['Close'].iloc[i]):.2f}",
                    'Shares': f"{shares:.2f}",
                    'Transaction Amount': f"{transaction_amount:.2f}",
                    'Gain/Loss': f"{gain_loss:.2f}",
                    'Balance': f"{balance:.2f}"
                })
                transactions.append({
                    'Date': data.index[i],
                    'Action': 'Sell',
                    'Price': data['Close'].iloc[i]
                })
                shares = Decimal(0)

    # Calculate final metrics
    total_gain_loss, total_return, annual_return = calculate_final_metrics(balance, initial_balance, data)

    # Add summary row
    add_summary_row(trade_log, total_gain_loss, balance, total_return, annual_return)

    # Save trade log and transactions
    save_trade_data(trade_log, transactions)

# Dictionary of strategies
strategies = {
    "SMA Crossover": sma_crossover_strategy,
    "Bollinger Bands": bollinger_bands_strategy,
    "MACD": macd_strategy
}