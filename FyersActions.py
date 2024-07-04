import Auth
from fyers_apiv3.FyersWebsocket import data_ws
from datetime import date
import datetime
import pandas as pd
from FyersModel import FyersModelClass

class Fyers:

    def __init__(self, symbols):
        self.fyersModel = FyersModelClass().get_fyers()
        self.symbols = symbols
        self.access_token = Auth.get_access_token()
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
        symbols = self.symbols
        self.fyers.subscribe(symbols=symbols, data_type=data_type)
        self.fyers.keep_running()

    def start_web_socket(self):
        self.fyers.connect()

    def PlaceOrder(self,lastTradedPrice, buyOrSell):
        data = {
            "symbol": "NSE:BANKNIFTY2470352600CE",
            "qty": 15,
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