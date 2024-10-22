import pandas as pd
from decimal import Decimal, getcontext

# Set the precision for Decimal
getcontext().prec = 28

def sma_crossover_strategy(data, symbol, short_window=40, long_window=100, initial_balance=100000):
    # Calculate short and long moving averages
    data = data.copy()  # Ensure we are working on a copy of the data
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

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
    total_gain_loss = balance - Decimal(initial_balance)
    total_return = (balance / Decimal(initial_balance) - 1) * 100
    annual_return = Decimal(float(total_return) / (len(data) / 252))  # Assuming 252 trading days in a year

    # Add summary row
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

    # Convert trade log to DataFrame and save to CSV
    trade_log_df = pd.DataFrame(trade_log)
    trade_log_df.to_csv('results.csv', index=False)

    # Save the SMA data and transactions for plotting
    sma_data = data[['Short_MA', 'Long_MA']]
    transactions_df = pd.DataFrame(transactions)
    sma_data.to_csv('sma_data.csv')
    transactions_df.to_csv('transactions.csv')

    return data

# Dictionary of strategies
strategies = {
    "SMA Crossover": sma_crossover_strategy,
}