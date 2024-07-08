import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from BackTest.Strategy import FirstCandle

def convert_to_5m():
    df = pd.read_csv('/Users/administrator/PycharmProjects/SR_Algo/back excels/BN24-now.csv')
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    if df['datetime'].isnull().any():
        print("Warning: There are null values in the 'datetime' column.")
    df.set_index('datetime', inplace=True, drop=False)
    resampled_df = df.resample('5T').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    resampled_df['datetime'] = resampled_df.index
    resampled_df.reset_index(drop=True, inplace=True)

    return resampled_df

def get_day_wise_df(df):
    start_time = pd.Timestamp('09:15:00')
    end_time = pd.Timestamp('15:25:00')
    dfs = []
    for date in df['datetime'].dt.date.unique():
        # Filter data for the specific date and time range
        mask = (df['datetime'].dt.date == date) & (df['datetime'].dt.time >= start_time.time()) & (
                    df['datetime'].dt.time <= end_time.time())
        filtered_df = df[mask]

        # Append filtered DataFrame to the list
        dfs.append(filtered_df)
    return dfs


df = convert_to_5m()
# df = pd.read_csv('/Users/administrator/PycharmProjects/SR_Algo/back excels/BN23-BN24.csv')
dfs = get_day_wise_df(df)
target = 40
increment = 5
till = 300
pnl_df = pd.DataFrame(columns = ['datetime', 'pnl', 'running_sum', 'cut_time'])
runningSum = []
while target <= till:
    totalPnl = 0
    for aDf in dfs:
        if not aDf.empty:
            cut_time,pnl = FirstCandle.strategy(aDf, target)
            if pnl is not None:
                totalPnl += pnl
                new_row = pd.DataFrame({"datetime": [str(aDf["datetime"].iloc[0])], "pnl": [pnl], "running_sum": [totalPnl], 'cut_time': [cut_time]})
                pnl_df = pd.concat([pnl_df, new_row], ignore_index=True)
    # target += increment
    # runningSum.append(pnl_df.iloc[-1]['running_sum'])

# pnl_df['datetime'] = pd.to_datetime(pnl_df['datetime'])
# plt.figure(figsize=(12, 6))
# plt.plot(pnl_df['datetime'], pnl_df['pnl'], linestyle='-', color='b', label='PnL')
# plt.plot(pnl_df['datetime'], pnl_df['running_sum'], linestyle='-', color='r', label='Running Sum')
# plt.xlabel('Date')
# plt.ylabel('Value')
# plt.title('PnL and Running Sum Over Time')
# plt.legend()
# plt.grid(True)
# plt.show()

