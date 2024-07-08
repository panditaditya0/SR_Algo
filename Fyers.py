import Auth
from fyers_apiv3.FyersWebsocket import data_ws
from datetime import date
import datetime
import pandas as pd
from FyersModel import FyersModelClass

class Fyers:

    def __init__(self, symbols):
        self.fyersModel = FyersModelClass().get_fyers()
        self.symbol = symbols
        self.access_token = Auth.get_cached_access_token()
        self.fyers = data_ws.FyersDataSocket(
                access_token=self.access_token,
                log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
                litemode=True,  # Lite mode disabled. Set to True if you want a lite response.
                write_to_file=False,  # Save response in a log file instead of printing it.
                reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
                on_connect=self.onopen,  # Callback function to subscribe to data upon connection.
                on_close=self.onclose,  # Callback function to handle WebSocket connection close events.
                on_error=self.onerror,  # Callback function to handle WebSocket errors.
                on_message=self.onmessage  # Callback function to handle incoming messages from the WebSocket.
            )
        self.symbolLtpDict = {}
        for aSymbol in symbols:
            self. symbolLtpDict.update({aSymbol: 0})



    def onmessage(self,message):
        self.symbolLtpDict[message['symbol']] = message['ltp']

    def getLtp(self):
        return self.symbolLtpDict

    def onerror(message):
        print("Error:", message)

    def onclose(message):
        print("Connection closed:", message)

    def onopen(self):
        data_type = "SymbolUpdate"
        symbols = self.symbol
        self.fyers.subscribe(symbols=symbols, data_type=data_type)
        self.fyers.keep_running()

    def start_web_socket(self):
        self.fyers.connect()

    def candle_history(self, symbol, startDate, endDate):
        data = {"symbol": symbol,
                "resolution": "1",
                "date_format": "1",
                "range_from": startDate,
                "range_to": endDate,
                "cont_flag": "1"}
        history_data = self.fyersModel.history(data=data)
        cols = ["datetime", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame.from_dict(history_data["candles"])
        df.columns = cols
        df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
        df["datetime"] = df["datetime"].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
        df["datetime"] = df["datetime"].dt.tz_localize(None)
        df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%dT%H:%M:%S")
        return df

    # def five_ma():
    #     af = candle_history()
    #     last_traded_price = getLtp()
    #     af.iloc[-1, -2] = last_traded_price
    #     af["EMA_5"] = af["close"].ewm(span=14).mean()
    #     return af

    def PlaceOrder(self,lastTradedPrice, buyOrSell, symbol, qty):
        data = {
            "symbol": symbol,
            "qty": qty,
            "type": 1,
            "side": buyOrSell,
            "productType": "INTRADAY",
            "limitPrice": lastTradedPrice,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
            "orderTag": "tag1"
        }
        response = self.fyersModel.place_order(data=data)
        print(response)

    def previous_day_candle(self, symbol, startDate, endDate):
        data = {"symbol": symbol,
                "resolution": "D",
                "date_format": "1",
                "range_from": startDate[:10],
                "range_to": endDate[:10],
                "cont_flag": "1"}
        history_data = self.fyersModel.history(data=data)
        cols = ["datetime", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame.from_dict(history_data["candles"])
        df.columns = cols
        df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
        df["datetime"] = df["datetime"].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
        df["datetime"] = df["datetime"].dt.tz_localize(None)
        df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%dT%H:%M:%S")
        return df