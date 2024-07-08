from BT_1stCandle import get_day_wise_df
from BT_1stCandle import convert_to_5m
from Helper.StudyCandle import stratgy

df = convert_to_5m()
# df = pd.read_csv('/Users/administrator/PycharmProjects/SR_Algo/back excels/BN23-BN24.csv')
dfs = get_day_wise_df(df)

for aDf in dfs:
    if not aDf.empty:
        stratgy(aDf)

