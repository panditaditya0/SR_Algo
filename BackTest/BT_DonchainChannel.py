from Strategy.DonchainChannel import backtest
from Strategy.DonchainChannel import generate_signals
from Strategy.DonchainChannel import applyIndicatior
import pandas as pd
from BT_1stCandle import convert_to_5m

# dfs = get_day_wise_df(df)
df = pd.read_csv('/Users/administrator/PycharmProjects/SR_Algo/back excels/BN22-BN23.csv')
df = convert_to_5m()

df.dropna(inplace=True)

data = applyIndicatior(df)
data = generate_signals(data)
nifty_final_value = backtest(data)
print(f"Final portfolio value {nifty_final_value}")
