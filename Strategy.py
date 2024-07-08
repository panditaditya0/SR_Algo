from Fyers import Fyers
import time
from datetime import datetime, timedelta
import asyncio
import websockets
import random
import threading
import time
import json

message = {}


async def produce_data(websocket, path):
    global message
    while True:
        await websocket.send(json.dumps(message))
        await asyncio.sleep(1)


async def start_server():
    server = await websockets.serve(produce_data, "localhost", 8765)
    await server.wait_closed()


def get_stoploss_and_target(buyingPrice):
    stopLoss = (0.95 * buyingPrice)
    target = (1.03 * buyingPrice)
    return stopLoss, target


def print_n_log(self, message):
    print(message)


def strategy_for_opening_above_previous_day_high(self, fyers, init_data):
    index_symbol = init_data['index_symbol']
    call_symbol = init_data['call_symbol']
    put_symbol = init_data['put_symbol']
    previous_day_low = init_data['previous_day_low']
    previous_day_high = init_data['previous_day_high']
    qty = init_data['qty']
    isTradeOn = False
    bought_at = pnl = noOfTradesCompleted = target = buyingPrice = stopLoss = lastTradedPrice = call_ltp = put_ltp = 0
    log = symbol_bought = ""
    while noOfTradesCompleted < 1:
        time.sleep(0.2)
        newLTP = fyers.getLtp()
        index_ltp = newLTP[newLTP]
        if newLTP[call_symbol] != 0 and newLTP[call_symbol] != "":
            call_ltp = newLTP[call_symbol]
        if newLTP[put_symbol] != 0 and newLTP[put_symbol] != "":
            put_ltp = newLTP[put_symbol]
        if isTradeOn:
            pnl = (call_ltp - bought_at) * 45

        global message
        message = {"log": log,
                   "support": previous_day_low,
                   "resistance": previous_day_high,
                   "ltp1": index_ltp,
                   "ltp2": call_ltp,
                   "ltp3": put_ltp,
                   "symbol1": index_symbol,
                   "symbol2": call_symbol,
                   "symbol3": put_symbol,
                   "pnl": pnl,
                   "bought_symbol": symbol_bought,
                   "bought_at": bought_at,
                   "datetime": str(datetime.now())
                   }

        # self.update.emit({"log": log,
        #                   "support": previous_day_low,
        #                   "resistance": previous_day_high,
        #                   "ltp1": index_ltp,
        #                   "ltp2": call_ltp,
        #                   "ltp3": put_ltp,
        #                   "symbol1": index_symbol,
        #                   "symbol2": call_symbol,
        #                   "symbol3": put_symbol,
        #                   "pnl" : pnl,
        #                   "bought_symbol": symbol_bought,
        #                   "bought_at": bought_at})
        log = ""
        if index_ltp <= previous_day_high and not isTradeOn:
            isTradeOn = True
            fyers.PlaceOrder(call_ltp, 1, call_symbol, qty)
            symbol_bought = call_symbol
            bought_at = call_ltp
            stopLoss, target = get_stoploss_and_target(call_ltp)
            log = f"Bought CALL at {bought_at} target = {target} stopLoss = {stopLoss}"
            print(log)

        if isTradeOn and call_ltp > target:
            fyers.PlaceOrder(call_ltp, -1, symbol_bought, qty)
            noOfTradesCompleted += 1
            print(f"Sold at PROFIT {pnl}")
            return pnl

        if isTradeOn and call_ltp < stopLoss:
            fyers.PlaceOrder(call_ltp, -1, symbol_bought, qty)
            noOfTradesCompleted += 1
            print(f"Sold at LOSS {pnl}")
            return pnl


def strategy_for_opening_below_previous_day_low(self, fyers, init_data):
    index_symbol = init_data['index_symbol']
    call_symbol = init_data['call_symbol']
    put_symbol = init_data['put_symbol']
    previous_day_low = init_data['previous_day_low']
    previous_day_high = init_data['previous_day_high']
    qty = init_data['qty']
    isTradeOn = False
    bought_at = pnl = noOfTradesCompleted = target = buyingPrice = stopLoss = lastTradedPrice = call_ltp = put_ltp = 0
    log = symbol_bought = ""
    while noOfTradesCompleted < 1:
        time.sleep(0.2)
        newLTP = fyers.getLtp()
        index_ltp = newLTP[index_symbol]
        if newLTP[call_symbol] != 0 and newLTP[call_symbol] != "":
            call_ltp = newLTP[call_symbol]
        if newLTP[put_symbol] != 0 and newLTP[put_symbol] != "":
            put_ltp = newLTP[put_symbol]
        if isTradeOn:
            pnl = (put_ltp - bought_at) * 45

        global message
        message = {"log": log,
                   "support": previous_day_low,
                   "resistance": previous_day_high,
                   "ltp1": index_ltp,
                   "ltp2": call_ltp,
                   "ltp3": put_ltp,
                   "symbol1": index_symbol,
                   "symbol2": call_symbol,
                   "symbol3": put_symbol,
                   "pnl": pnl,
                   "bought_symbol": symbol_bought,
                   "bought_at": bought_at,
                   "datetime": str(datetime.now())}

        # self.update.emit({"log": log,
        #                   "support": previous_day_low,
        #                   "resistance": previous_day_high,
        #                   "ltp1": index_ltp,
        #                   "ltp2": call_ltp,
        #                   "ltp3": put_ltp,
        #                   "symbol1": index_symbol,
        #                   "symbol2": call_symbol,
        #                   "symbol3": put_symbol,
        #                   "pnl": pnl,
        #                   "bought_symbol": symbol_bought,
        #                   "bought_at": bought_at})
        log = ""
        if index_ltp >= previous_day_low and not isTradeOn:
            isTradeOn = True
            fyers.PlaceOrder(put_ltp, 1, call_symbol, qty)
            symbol_bought = put_symbol
            bought_at = put_ltp
            stopLoss, target = get_stoploss_and_target(put_ltp)
            log = f"Bought CALL at {bought_at} target = {target} stopLoss = {stopLoss}"
            print(log)

        if isTradeOn and put_ltp > target:
            fyers.PlaceOrder(put_ltp, -1, symbol_bought, qty)
            noOfTradesCompleted += 1
            print(f"Sold at PROFIT {pnl}")
            return pnl

        if isTradeOn and put_ltp < stopLoss:
            fyers.PlaceOrder(put_ltp, -1, symbol_bought, qty)
            noOfTradesCompleted += 1
            print(f"Sold at LOSS {pnl}")
            return pnl


def strategy_for_opening_btw_previous_high_low(self, fyers, init_data):
    index_symbol = init_data['index_symbol']
    call_symbol = init_data['call_symbol']
    put_symbol = init_data['put_symbol']
    previous_day_low = init_data['previous_day_low']
    previous_day_high = init_data['previous_day_high']
    qty = init_data['qty']
    isTradeOn = False
    bought_at = pnl = noOfTradesCompleted = target = baught_instrument_ltp = stopLoss = lastTradedPrice = call_ltp = put_ltp = 0
    log = symbol_bought = ""
    while noOfTradesCompleted < 1:
        time.sleep(0.2)
        newLTP = fyers.getLtp()
        index_ltp = newLTP[index_symbol]
        if newLTP[call_symbol] != 0 and newLTP[call_symbol] != "":
            call_ltp = newLTP[call_symbol]
        if newLTP[put_symbol] != 0 and newLTP[put_symbol] != "":
            put_ltp = newLTP[put_symbol]
        if isTradeOn:
            pnl = (baught_instrument_ltp - bought_at) * qty

        global message
        message = {"log": log,
                   "support": previous_day_low,
                   "resistance": previous_day_high,
                   "ltp1": index_ltp,
                   "ltp2": call_ltp,
                   "ltp3": put_ltp,
                   "symbol1": index_symbol,
                   "symbol2": call_symbol,
                   "symbol3": put_symbol,
                   "pnl": pnl,
                   "bought_symbol": symbol_bought,
                   "bought_at": bought_at,
                   "datetime": str(datetime.now())}

        # self.update.emit({"log": log,
        #                   "support": previous_day_low,
        #                   "resistance": previous_day_high,
        #                   "ltp1": index_ltp,
        #                   "ltp2": call_ltp,
        #                   "ltp3": put_ltp,
        #                   "symbol1": index_symbol,
        #                   "symbol2": call_symbol,
        #                   "symbol3": put_symbol,
        #                   "pnl": pnl,
        #                   "bought_symbol": symbol_bought,
        #                   "bought_at": bought_at})
        log = ""

        if index_ltp <= previous_day_low and not isTradeOn:
            isTradeOn = True
            fyers.PlaceOrder(call_ltp, 1, call_symbol, qty)
            symbol_bought = call_symbol
            bought_at = call_ltp = baught_instrument_ltp
            stopLoss, target = get_stoploss_and_target(baught_instrument_ltp)
            log = f"Bought CALL at {bought_at} target = {target} stopLoss = {stopLoss}"
            print(log)

        if index_ltp >= previous_day_high and not isTradeOn:
            isTradeOn = True
            fyers.PlaceOrder(put_ltp, 1, put_symbol, qty)
            symbol_bought = put_symbol
            bought_at = put_ltp = baught_instrument_ltp
            stopLoss, target = get_stoploss_and_target(baught_instrument_ltp)
            log = f"Bought PUT at {bought_at} target = {target} stopLoss = {stopLoss}"
            print(log)

        if isTradeOn:
            if symbol_bought == call_symbol:
                if call_ltp > target:
                    fyers.PlaceOrder(call_ltp, -1, symbol_bought, qty)
                    noOfTradesCompleted += 1
                    print(f"Sold put on PROFIT {pnl}")
                    return pnl
                if call_ltp < stopLoss:
                    fyers.PlaceOrder(call_ltp, -1, symbol_bought, qty)
                    noOfTradesCompleted += 1
                    print(f"Sold put on LOSS {pnl}")
                    return pnl

            if symbol_bought == put_symbol:
                if put_ltp > target:
                    fyers.PlaceOrder(put_ltp, -1, symbol_bought, qty)
                    noOfTradesCompleted += 1
                    print(f"Sold put on PROFIT {pnl}")
                    return pnl
                if put_ltp < stopLoss:
                    fyers.PlaceOrder(put_ltp, -1, symbol_bought, qty)
                    noOfTradesCompleted += 1
                    print(f"Sold put on LOSS {pnl}")
                    return pnl


def strategy(previousDayCandle, self):
    qty = 45
    previous_day_low = float(previousDayCandle['low'])
    previous_day_high = float(previousDayCandle['high'])
    # index_symbol = "NSE:NIFTYBANK-INDEX"
    # call_symbol = f"NSE:BANKNIFTY24710{(round(previous_day_low / 100) * 100) - 100}CE"
    # put_symbol = f"NSE:BANKNIFTY24710{(round(previous_day_high / 100) * 100) + 100}PE"

    index_symbol = "MCX:CRUDEOILM24JULFUT"
    call_symbol = "MCX:CRUDEOILM24JULFUT"
    put_symbol = "MCX:CRUDEOILM24JULFUT"
    init_data = {
        'previous_day_low': previous_day_low,
        'previous_day_high': previous_day_high,
        'index_symbol': index_symbol,
        'call_symbol': call_symbol,
        'put_symbol': put_symbol,
        'qty': qty
    }
    fyers = Fyers([index_symbol, call_symbol, put_symbol])
    fyers.start_web_socket()
    time.sleep(3)
    newLTP = fyers.getLtp()
    index_ltp = newLTP[index_symbol]
    if index_ltp > previous_day_high:
        pnl = strategy_for_opening_above_previous_day_high(self, fyers, init_data)
        return pnl
    elif index_ltp < previous_day_low:
        pnl = strategy_for_opening_below_previous_day_low(self, fyers, init_data)
        return pnl
    else:
        pnl = strategy_for_opening_btw_previous_high_low(self, fyers, init_data)
        return pnl


def start_strategy(self):
    fy = Fyers("NSE:NIFTYBANK-INDEX")
    day_b4_yestarday = datetime.now() - timedelta(6)
    df = fy.previous_day_candle("NSE:NIFTYBANK-INDEX", str(day_b4_yestarday), str(datetime.now()))
    previous_day_candle = df.iloc[df.__len__() - 2]
    strategy(previous_day_candle, self)


def produce_data_thread():
    global message
    start_strategy("self")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_thread = threading.Thread(target=lambda: asyncio.run(start_server()))
    server_thread.start()
    produce_data_thread()
    server_thread.join()
