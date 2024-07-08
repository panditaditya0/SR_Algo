import datetime

def strategy(df, previousDayCandle, target):
    previous_day_high =float(previousDayCandle.iloc[0]['high'])
    previous_day_low = float(previousDayCandle.iloc[0]['low'])
    starting_ltp = float(df.iloc[0]['open'])

    length = len(df.index)
    count = 1
    side =""
    bought_at=0
    sl = 100
    is_trade_taken = False

    if starting_ltp > previous_day_high:
        while count < length:
            currentCandle = df.iloc[count]
            current_open = float(currentCandle["open"])
            current_high = float(currentCandle["high"])
            current_low = float(currentCandle["low"])
            current_close = float(currentCandle["close"])
            count = count + 1
            if current_open < previous_day_high or current_high<previous_day_high or current_low< previous_day_high or current_close < previous_day_high:
                if not is_trade_taken:
                    if current_low <= previous_day_low:
                        side = "call"
                        is_trade_taken = True
                        bought_at = previous_day_low
                        continue

                if is_trade_taken:
                    if side == "call":
                        diff_1 = bought_at - current_close
                        diff_2 = bought_at - current_high
                        diff_3 = bought_at - current_open
                        diff_4 = bought_at - current_low

                        if diff_1 < target * -1 or diff_2 < target * -1 or diff_3 < target * -1 or diff_4 < target * -1:
                            pnl = max(diff_1 * -1, diff_2 * -1, diff_3 * -1, diff_4 * -1)
                            return int(round(pnl))
                        if diff_1 > sl or diff_2 > sl or diff_3 > sl or diff_4 > sl:
                            pnl = min(diff_1, diff_2, diff_3, diff_4)
                            return int(round(pnl))


    if starting_ltp < previous_day_low:
        while count < length:
            currentCandle = df.iloc[count]
            current_open = float(currentCandle["open"])
            current_high = float(currentCandle["high"])
            current_low = float(currentCandle["low"])
            current_close = float(currentCandle["close"])
            count = count + 1
            if current_open > previous_day_low or current_high>previous_day_low or current_low> previous_day_low or current_close > previous_day_low:
                if not is_trade_taken:
                    if current_high >= previous_day_high:
                        side = "put"
                        bought_at = previous_day_high
                        is_trade_taken = True
                        continue
                if is_trade_taken:
                    if side == "put":
                        diff_1 = bought_at - current_close
                        diff_2 = bought_at - current_high
                        diff_3 = bought_at - current_open
                        diff_4 = bought_at - current_low
                        if diff_1 > target or diff_2 > target or diff_3 > target or diff_4 > target:
                            pnl = max(diff_1, diff_2, diff_3, diff_4)
                            return int(round(pnl))

                        if diff_1 < sl * -1 or diff_2 < sl * -1 or diff_3 < sl * -1 or diff_4 < sl * -1:
                            pnl = min(diff_1, diff_2, diff_3, diff_4)
                            return int(round(pnl))

    while count < length:
        currentCandle = df.iloc[count]
        current_open = float(currentCandle["open"])
        current_high = float(currentCandle["high"])
        current_low = float(currentCandle["low"])
        current_close = float(currentCandle["close"])
        count = count + 1
        if not is_trade_taken:
            if current_high >= previous_day_high:
                side = "put"
                bought_at = previous_day_high
                is_trade_taken = True
                continue

            if current_low <= previous_day_low:
                side = "call"
                is_trade_taken = True
                bought_at = previous_day_low
                continue

        if is_trade_taken:
            if side == "call":
                diff_1 = bought_at - current_close
                diff_2 = bought_at - current_high
                diff_3 = bought_at - current_open
                diff_4 = bought_at - current_low

                if diff_1 < target*-1 or diff_2 < target*-1 or diff_3 < target*-1 or diff_4 < target*-1:
                    pnl = max(diff_1*-1,diff_2*-1, diff_3*-1 ,diff_4*-1)
                    return int(round(pnl))
                if diff_1 > sl or diff_2 > sl or diff_3 > sl or diff_4 > sl:
                    pnl = min(diff_1,diff_2, diff_3 ,diff_4)
                    return int(round(pnl))

            if side == "put":
                diff_1 = bought_at - current_close
                diff_2 = bought_at - current_high
                diff_3 = bought_at - current_open
                diff_4 = bought_at - current_low
                if diff_1 > target or diff_2 > target or diff_3 > target or diff_4 > target:
                    pnl = max(diff_1,diff_2, diff_3 ,diff_4)
                    return int(round(pnl))

                if diff_1 < sl*-1 or diff_2 < sl*-1 or diff_3 < sl*-1 or diff_4 < sl*-1:
                    pnl = min(diff_1, diff_2, diff_3, diff_4)
                    return int(round(pnl))
