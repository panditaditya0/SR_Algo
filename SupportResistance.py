import time
from Fyers import Fyers

def supportAndResistance(sup, res, self):
    # index_symbol = "NSE:NIFTYBANK-INDEX"
    # call_symbol = f"NSE:BANKNIFTY24710{(round(sup / 100) * 100) - 100}CE"
    # put_symbol = f"NSE:BANKNIFTY24710{(round(res / 100) * 100) + 100}PE"
    index_symbol = "MCX:CRUDEOILM24JULFUT"
    call_symbol ="MCX:CRUDEOILM24JULFUT"
    put_symbol = "MCX:CRUDEOILM24JULFUT"
    qty = 45
    fyers = Fyers([index_symbol, call_symbol, put_symbol])
    fyers.start_web_socket()
    time.sleep(3)
    isTradeOn = False
    target = buyingPrice = stopLoss = lastTradedPrice = call_ltp = put_ltp = 0
    symbol_bought = ""
    bought_at =0
    pnl = 0
    log = ""
    noOfTradesCompleted = 0
    while noOfTradesCompleted < 1:
        time.sleep(0.2)
        newLTP = fyers.getLtp()
        index_ltp = newLTP[index_symbol]
        if newLTP[call_symbol] != 0 and newLTP[call_symbol] != "":
            call_ltp = newLTP[call_symbol]
        if newLTP[put_symbol] != 0 and newLTP[put_symbol] != "":
            put_ltp = newLTP[put_symbol]
        if isTradeOn:
            pnl = (buyingPrice - bought_at) * 45
        self.update.emit({"log": log,
                          "support": sup,
                          "resistance": res,
                          "ltp1": index_ltp,
                          "ltp2": call_ltp,
                          "ltp3": put_ltp,
                          "symbol1": index_symbol,
                          "symbol2": call_symbol,
                          "symbol3": put_symbol,
                          "pnl" : pnl,
                          "bought_symbol": symbol_bought,
                          "bought_at": bought_at})
        log = ""

        if index_ltp != lastTradedPrice:
            lastTradedPrice = float(index_ltp)
            # ltpData = f"{datetime.time} -> ltp {index_ltp} tradeOn -> {isTradeOn}  symbol -> {symbol_bought} at {buyingPrice} sl {stopLoss} target {target}"
            # self.update.emit({"ltpData": ltpData})
            # print(ltpData)
            if lastTradedPrice < sup and not isTradeOn:
                fyers.PlaceOrder(call_ltp, 1, call_symbol, qty)
                buyingPrice = call_ltp
                stopLoss, target = get_stoploss_and_target(buyingPrice)
                # self.update.emit({"log",f"Trade TAKEN at -> {buyingPrice} SL -> {stopLoss} TARGET -> {target}"})
                isTradeOn = True
                symbol_bought = call_symbol
                bought_at = call_ltp
                log = f"Bought CALL at {bought_at} target = {target} stopLoss = {stopLoss}"

            if lastTradedPrice > res and not isTradeOn:
                fyers.PlaceOrder(put_ltp, 1, put_symbol, qty)
                buyingPrice = put_ltp
                stopLoss, target = get_stoploss_and_target(buyingPrice)
                print_n_log(self, {"log",f"Trade TAKEN at -> {buyingPrice} SL -> {stopLoss} TARGET -> {target}"})
                isTradeOn = True
                symbol_bought = put_symbol
                bought_at = put_ltp
                log = f"Bought PUT at {bought_at} target = {target} stopLoss = {stopLoss}"
                # dataLabel.setText()

            if isTradeOn:
                if symbol_bought == call_symbol:
                    buyingPrice = call_ltp
                elif symbol_bought == put_symbol:
                    buyingPrice = put_ltp

            if isTradeOn and stopLoss > buyingPrice:
                fyers.PlaceOrder(buyingPrice, -1, symbol_bought, qty)
                print_n_log(self, f"SOLD AT LOSS -> {stopLoss}")
                isTradeOn = False
                stopLoss = target = buyingPrice = 0
                symbol_bought = ''
                noOfTradesCompleted = noOfTradesCompleted+1
                # dataLabel.setText(f"s -> {sup} \n res -> {res} \n tradeOn -> {isTradeOn} \n  SOLD AT SL")

            if isTradeOn and buyingPrice > target:
                fyers.PlaceOrder(buyingPrice, -1, symbol_bought, qty)
                print_n_log(self, f"SOLD AT PROFIT -> {target}")
                isTradeOn = False
                stopLoss = target = buyingPrice = 0
                symbol_bought = ''
                # dataLabel.setText(f"s -> {sup} \n res -> {res} \n tradeOn -> {isTradeOn} \n  SOLD AT TARGET")
                noOfTradesCompleted = noOfTradesCompleted+1

    return pnl

def get_stoploss_and_target(buyingPrice):
    stopLoss = (0.95 * buyingPrice)
    target = (1.03 * buyingPrice)
    return stopLoss, target


def print_n_log(self, message):
    print(message)
    # self.update.emit(message)
