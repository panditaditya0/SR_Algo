import datetime

def strategy(df, target):
    first_three_entries = df.head(6)
    trigger_high = float(first_three_entries['high'].max())
    trigger_low = float(first_three_entries['low'].min())
    # a=df.iloc[0]
    # trigger_high = float(a["high"])
    # trigger_low = float(a["low"])
    isTradeTaken = False
    count = 7
    baughtAt = 0
    side = ""
    pnl = 0
    sl = 0
    while count <=len(df.index)-7:
        currentCandle = df.iloc[count]
        current_open = float(currentCandle["open"])
        current_high = float(currentCandle["high"])
        current_low = float(currentCandle["low"])
        current_close = float(currentCandle["close"])
        count = count + 1
        if not isTradeTaken:
            if trigger_high < current_open or trigger_high < current_high or trigger_high <  current_low or  trigger_high <  current_close:
                baughtAt = trigger_high
                sl = trigger_low
                side = "call"
                isTradeTaken = True
                continue

            if trigger_low > current_open or trigger_low > current_high or trigger_low >  current_low or  trigger_low >  current_close:
                baughtAt = trigger_low
                sl = trigger_high
                side = "put"
                isTradeTaken = True
                continue

        if isTradeTaken:
            if side == "call":
                if baughtAt - sl > 100:
                    return str(currentCandle['datetime']),sl-baughtAt

                if current_open < sl or current_high < sl or current_low < sl  or current_close < sl :
                    return str(currentCandle['datetime']),baughtAt - sl

                diff1 = (current_open - baughtAt) > target
                diff2 = (current_high - baughtAt) > target
                diff3 = (current_low  - baughtAt) > target
                diff4 = (current_close - baughtAt) > target
                if diff1 or diff2 or diff3 or diff4:
                    return str(currentCandle['datetime']),target

            if side == "put":
                if baughtAt - sl > 100:
                    return str(currentCandle['datetime']),baughtAt - sl

                if current_open > sl or current_high > sl or current_low > sl  or current_close > sl:
                    return str(currentCandle['datetime']),baughtAt - sl

                diff1 = (baughtAt- current_open) > target
                diff2 = (baughtAt-current_high) > target
                diff3 = (baughtAt-current_low) > target
                diff4 = (baughtAt-current_close) > target
                if diff1 or diff2 or diff3 or diff4:
                    return str(currentCandle['datetime']),target
    return None, None