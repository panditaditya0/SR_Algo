import pandas as pd
from BackTest.Strategy import LastDayHighLow
from Helper import StudyCandle


def get_profit_and_loss_streaks(data):
    if not data:
        return [], []

    profit_streaks = []
    loss_streaks = []

    current_streak_type = 'profit' if data[0] > 0 else 'loss'
    current_streak_count = 1

    for value in data[1:]:
        if (value > 0 and current_streak_type == 'profit') or (value < 0 and current_streak_type == 'loss'):
            current_streak_count += 1
        else:
            if current_streak_type == 'profit':
                profit_streaks.append(current_streak_count)
            else:
                loss_streaks.append(current_streak_count)
            current_streak_type = 'profit' if value > 0 else 'loss'
            current_streak_count = 1

    # Append the last streak
    if current_streak_type == 'profit':
        profit_streaks.append(current_streak_count)
    else:
        loss_streaks.append(current_streak_count)

    return profit_streaks, loss_streaks

def get_day_wise_df(df):
    start_time = pd.Timestamp('09:15:00')
    end_time = pd.Timestamp('15:25:00')
    dfs = []
    for date in df['datetime'].dt.date.unique():
        mask = (df['datetime'].dt.date == date) & (df['datetime'].dt.time >= start_time.time()) & (
                df['datetime'].dt.time <= end_time.time())
        filtered_df = df[mask]
        dfs.append(filtered_df)
    return dfs

def no_of_loss_profity_days(pnls):
    loss_count = 0
    profit_count = 0

    for pnl in pnls:
        if pnl is not None:
            if pnl > 0:
                profit_count += 1
            else:
                loss_count += 1
    return loss_count, profit_count

def get_max_profit_and_loss_in_a_row(data):
    max_profit = 0
    max_loss = 0

    current_profit = 0
    current_loss = 0

    for value in data:
        if value > 0:
            current_profit += value
            current_loss = 0
        else:
            current_loss += value
            current_profit = 0

        max_profit = max(max_profit, current_profit)
        max_loss = min(max_loss, current_loss)

    return max_profit, max_loss


df = pd.read_csv('/Users/administrator/PycharmProjects/SR_Algo/back excels/BN24-now.csv')
df = StudyCandle.candle_resampler(df, '1T')
df.dropna(inplace=True)
dfs = get_day_wise_df(df)
pnl_df = pd.DataFrame(columns=['datetime', 'pnl', 'running_sum', 'cut_time'])
runningSum = 0
length_of_days = dfs.__len__()
counter = 0
pnls = []
target = 70
while (length_of_days - 1) > counter:
    if counter == 212:
        print("d")
    previous_day_candle = StudyCandle.candle_resampler(dfs[counter], 'D')
    if len(dfs[counter + 1]) > 0:
        day_pnl = LastDayHighLow.strategy(dfs[counter + 1], previous_day_candle, target)
        if day_pnl is not None:
            pnls.append(day_pnl)
            runningSum += day_pnl
    else:
        counter += 1
    counter += 1

profit_streaks, loss_streaks = get_profit_and_loss_streaks(pnls)
loss_count, profit_count = no_of_loss_profity_days(pnls)
max_profit, max_loss = get_max_profit_and_loss_in_a_row(pnls)

print(runningSum)
print(pnls)
print("No of trading days: ", len(pnls))
print("Max draw down: ", max_loss)
print("Max profit: ", max_profit)
print("No of loss days: ", loss_count)
print("No of profit days: ", profit_count)
print("Max Profit :", max(pnls))
print("Max Loss: ", min(pnls))
print("Profit streaks: ", max(profit_streaks))
print("Loss streaks: ", max(loss_streaks))
print("Average profit/loss in a day: ", runningSum / len(pnls))