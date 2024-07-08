import time

import PivotPointStd
from Fyers import Fyers
from datetime import datetime, timedelta
import pandas as pd
import os

def append_df_to_csv(filename, df):
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', index=False, header=False)


def get_dates_every_75_days():
    start_date = pd.Timestamp('2022-01-01')
    end_date = pd.Timestamp('2022-12-31')
    segments = []
    while start_date <= end_date:
        segment_end = start_date + timedelta(days=74)
        if segment_end > end_date:
            segment_end = end_date
        segments.append((start_date, segment_end))
        start_date = segment_end + timedelta(days=1)
    return segments


# Example usage
dates = get_dates_every_75_days()
fy = Fyers(["NSE:NIFTYBANK-INDEX"])
length = dates.__len__()
for index, aDate in enumerate(dates):
    df = fy.candle_history("NSE:NIFTYBANK-INDEX", dates[index][0].strftime("%Y-%m-%d"), dates[index][1].strftime("%Y-%m-%d"))
    append_df_to_csv('BN22-BN23.csv', df)


