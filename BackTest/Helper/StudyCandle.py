
import pandas as pd


def candle_resampler(newDf, sample_time):
    df =  newDf.copy()
    # Ensure the 'datetime' column exists
    if 'datetime' not in df.columns:
        raise KeyError("The DataFrame does not contain a 'datetime' column.")

    # Convert 'datetime' column to datetime objects and handle errors
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    if df['datetime'].isnull().any():
        print("Warning: There are null values in the 'datetime' column.")

    # Set 'datetime' as the index for resampling
    df.set_index('datetime', inplace=True)

    # Resample the DataFrame
    resampled_df = df.resample(sample_time).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    # Add 'datetime' column back and reset index
    resampled_df['datetime'] = resampled_df.index
    resampled_df.reset_index(drop=True, inplace=True)

    return resampled_df

def typeOfCandle(candle):
    candle_high = candle["high"]
    candle_low = candle["low"]
    candle_close = candle["close"]
    candle_mid = (candle_high/2)+(candle_low/2)
    delta_close_to_mid = candle_mid-candle_close
    candle_size = candle_high - candle_low
    delta_percentage = (delta_close_to_mid/candle_size) * 100
    if delta_close_to_mid > 0:
        if  delta_percentage > 10:
            return "very bearish"
        return "bearish"
    if  delta_close_to_mid <0:
        delta_percentage = delta_percentage* -1
        if delta_percentage > 10:
            return "very bullish"
        return "bullish"
    else:
        return "neutral"

def stratgy(df):
    count = 13
    while count <=len(df.index)-7:
        currentCandle = df.iloc[count]
        typeOfCandle(currentCandle)
        count+=1
