from Fyers import Fyers
import time
from datetime import datetime, timedelta

open = None
high = None
low = None
close = None
ltp_values= []


def getCandle():
    global ltp_values
    ltp_list = ltp_values
    if ltp_list.__len__() > 1:
        open = ltp_list[0]
        high = max(ltp_list)
        low = min(ltp_list)
        close = ltp_list[-1]

        return {
            'Open': open,
            'High': high,
            'Low': low,
            'Close': close
        }
    return None

def convert_ltp_to_ohlc(ltp_list):
    if not ltp_list:
        return None

    open = ltp_list[0]
    high = max(ltp_list)
    low = min(ltp_list)
    close = ltp_list[-1]

    return {
        'Open': open,
        'High': high,
        'Low': low,
        'Close': close
    }

def get_round_start_time():
    now = datetime.now()
    # Round the current time to the nearest previous 5-minute mark
    minute = (now.minute // 5) * 5
    start_time = now.replace(minute=minute, second=0, microsecond=0)
    return start_time


def collect_ltp_for_5_minutes(start_time, symbol, fy):
    end_time = start_time + timedelta(minutes=5)
    while datetime.now() < end_time:
        current_ltp =fy.getLtp()
        try:
            global ltp_values
            if current_ltp['MCX:CRUDEOILM24JULFUT'] == 0:
                continue
            if ltp_values.__len__() == 0 :
                ltp_values.append(current_ltp['MCX:CRUDEOILM24JULFUT'])

            if ltp_values[-1] != current_ltp['MCX:CRUDEOILM24JULFUT']:
                ltp_values.append(current_ltp['MCX:CRUDEOILM24JULFUT'])
        except:
            print(f"Error while  making  candle {symbol}")
        time.sleep(0.1)
    return ltp_values

def start_making_candles(symbol):
    fy = Fyers(symbol)
    fy.start_web_socket()
    global ltp_values
    while True:
        ltp_values = []
        start_time = get_round_start_time()
        collect_ltp_for_5_minutes(start_time,symbol, fy)

def get_current_candle():
    return convert_ltp_to_ohlc(ltp_values)

















