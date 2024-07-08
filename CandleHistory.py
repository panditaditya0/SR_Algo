import time

import PivotPointStd
from Fyers import Fyers
from datetime import datetime, timedelta

df = None
def get_round_start_time():
    now = datetime.now()
    minute = (now.minute // 5) * 5
    start_time = now.replace(minute=minute, second=0, microsecond=0)
    return start_time

def start_updating_history_candles(symbol):
    fy = Fyers(symbol)
    global df
    df = fy.candle_history(symbol[0])
    while True:
        start_time = get_round_start_time()
        latest_candle = PivotPointStd.getCandle()
        if latest_candle == None:
            continue
        if(str(df.iloc[-1, 0])  == str(start_time)):
            if float(df.iloc[-1, 2]) < float(latest_candle['High']):
                df.iloc[-1, 2] = latest_candle['High']
            if float(df.iloc[-1, 3]) > float(latest_candle['Low']):
                df.iloc[-1, 3] = latest_candle['Low']
            df.iloc[-1, 4] = latest_candle['Close']
        else:
            df._append(start_time, latest_candle["Open"], latest_candle["High"], latest_candle["Low"], latest_candle["Close"])
    time.sleep(0.2)


def get_candle_history():
    return df
