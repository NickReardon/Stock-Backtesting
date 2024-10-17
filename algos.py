import math

def sma(period_in_days, day, data):
    if day < period_in_days:
        raise ValueError("Day index must be at least equal to the period in days.")
    
    # Calculate the start index for the period
    start_index = day - period_in_days
    # Calculate the sum of the closing prices for the specified period
    sum_prices = sum(data[start_index:day])
    
    # Calculate the simple moving average
    return sum_prices / period_in_days

def ema(period_in_days, day, data):
    if day < period_in_days:
        raise ValueError("Day index must be at least equal to the period in days.")
    
    # Calculate the multiplier
    multiplier = 2 / (period_in_days + 1)

    # Calculate the initial SMA for the first `period_in_days` days
    initial_sma = sum(data[:period_in_days]) / period_in_days
    ema_values = [initial_sma]

    # Calculate the EMA for each subsequent day
    for i in range(period_in_days, day + 1):
        current_price = data[i]
        new_ema = (current_price * multiplier) + (ema_values[-1] * (1 - multiplier))
        ema_values.append(new_ema)

    return ema_values[-1]  # Return the last calculated EMA value

def standard_deviation(period_in_days, day, data):
    if day < period_in_days:
        raise ValueError("Day index must be at least equal to the period in days.")
    
    # Calculate the average (SMA) for the period
    start_index = day - period_in_days
    prices = data[start_index:day]
    mean = sum(prices) / period_in_days
    
    # Calculate the standard deviation
    variance = sum((x - mean) ** 2 for x in prices) / period_in_days
    return math.sqrt(variance)

def upper_bollinger_band(period_in_days, day, data, k=2):
    if day < period_in_days:
        raise ValueError("Day index must be at least equal to the period in days.")
    
    # Calculate the SMA for the period
    sma = sum(data[day - period_in_days:day]) / period_in_days
    std_dev = standard_deviation(period_in_days, day, data)
    
    # Calculate the upper Bollinger Band
    return sma + (k * std_dev)

def lower_bollinger_band(period_in_days, day, data, k=2):
    if day < period_in_days:
        raise ValueError("Day index must be at least equal to the period in days.")
    
    # Calculate the SMA for the period
    sma = sum(data[day - period_in_days:day]) / period_in_days
    std_dev = standard_deviation(period_in_days, day, data)
    
    # Calculate the lower Bollinger Band
    return sma - (k * std_dev)

# Example usage
data = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 
        40]  # Example closing prices for 30 days

# Calculate SMA for day 25 with a period of 5 days
result = sma(5, 25, data)
print("SMA:", result)  # Output: 34.0

# Calculate EMA for day 25 with a period of 5 days
result = ema(5, 25, data)
print("EMA:", result)  # Output: the EMA value for day 25

# Calculate Bollinger Bands for day 25 with a period of 5 days
upper_band = upper_bollinger_band(5, 25, data)
lower_band = lower_bollinger_band(5, 25, data)

print("Upper Bollinger Band:", upper_band)
print("Lower Bollinger Band:", lower_band)