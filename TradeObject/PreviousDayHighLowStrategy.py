class PreviousDayHighLowStrategy:
    def __init__(self, fyers):
        self.qty = 45
        self.isTradeOn = False
        self.noOfTradesCompleted = self.pnl = self.bought_at = self.target = self.buyingPrice = self.stopLoss = self.lastTradedPrice = self.call_ltp = self.put_ltp = 0
        self.log = self.symbol_bought = ''
        self.fyers = fyers
    def get_index_ltp(self):
        newLTP = self.fyers.getLtp()

