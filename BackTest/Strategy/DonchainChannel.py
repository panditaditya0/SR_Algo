import pandas as pd
import numpy as np


# Calculate Donchian Channel
def donchian_channel(data, window):
    data['donchian_upper'] = data['high'].rolling(window=window).max()
    data['donchian_lower'] = data['low'].rolling(window=window).min()
    data['donchian_middle'] = (data['donchian_upper'] + data['donchian_lower']) / 2
    return data

# Calculate EMA
def ema(data, period):
    data['ema'] = data['close'].ewm(span=period, adjust=False).mean()
    return data


# Calculate RSI
def rsi(data, period):
    delta = data['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    data['rsi'] = 100 - (100 / (1 + rs))
    return data


def applyIndicatior(data):
    data = donchian_channel(data, 4)
    data = ema(data, 50)
    data = rsi(data, 14)
    return data


# Define the trading strategy
def generate_signals(data):
    data['buy_signal'] = ((data['high'] > data['donchian_upper'])).astype(int)
    data['sell_signal'] = ((data['low'] < data['donchian_lower'])).astype(int)
    return data

# Backtest the strategy
def backtest(data, initial_balance=100000):
    balance = initial_balance
    position = 0
    for index, row in data.iterrows():
        if row['buy_signal'] and position == 0:
            position = balance / row['close']
            balance = 0
            print(f"Buy at {row['datetime']} price {row['close']}")
        elif row['sell_signal'] and position > 0:
            balance = position * row['close']
            position = 0
            print(f"Sell at {row['datetime']} price {row['close']}")

    # Calculate final portfolio value
    final_value = balance + position * data.iloc[-1]['close']
    return final_value


