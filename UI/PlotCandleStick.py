import pandas as pd
import mplfinance as mpf
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import CandleHistory


#
# # Sample initial data
# data = {
#     'Date': [
#         datetime.datetime(2023, 1, 1),
#         datetime.datetime(2023, 1, 2),
#         datetime.datetime(2023, 1, 3),
#         datetime.datetime(2023, 1, 4),
#         datetime.datetime(2023, 1, 5)
#     ],
#     'Open': [100, 102, 104, 103, 105],
#     'High': [110, 108, 109, 107, 106],
#     'Low': [90, 95, 98, 92, 93],
#     'Close': [105, 100, 107, 104, 103]
# }
#
# # Create DataFrame
# df = pd.DataFrame(data)
# df.set_index('Date', inplace=True)
#
# # Function to simulate new data
# def generate_new_data(last_date):
#     new_date = last_date + datetime.timedelta(days=1)
#     open_price = np.random.randint(100, 110)
#     high_price = open_price + np.random.randint(0, 10)
#     low_price = open_price - np.random.randint(0, 10)
#     close_price = np.random.randint(low_price, high_price)
#     return {
#         'Date': new_date,
#         'Open': open_price,
#         'High': high_price,
#         'Low': low_price,
#         'Close': close_price
#     }

# Update function
def update(frame):
    global df
    df = CandleHistory.get_candle_history()
    plt.clf()
    mpf.plot(df, type='candle', style='charles', ax=plt.gca(), ylabel='Price')

def show():
    global df
    df = CandleHistory.get_candle_history()
    df.set_index('datetime', inplace=True)
    fig, ax = plt.subplots()
    mpf.plot(df, type='candle', style='charles', ax=ax, ylabel='Price')
    ani = FuncAnimation(fig, update, interval=1000)
    plt.show()
