import os
import pandas as pd

for filename in os.listdir('datasets/S&P500/'):  #read through all the files
    symbol = filename.split(".")[0]     #get the symbol of the stock
    df = pd.read_csv('datasets/S&P500/{}'.format(filename))     #reading the data
    if df.empty:        #if the dataframe is empty -> continue
        continue
    df['SMA'] = df['Close'].rolling(window = 20).mean()     #Simple Moving Average calculation (period = 20)
    df['stdev'] = df['Close'].rolling(window = 20).std()    #Standard Deviation calculation
    df['Lower_Bollinger'] = df['SMA'] - (2 * df['stdev'])   #Calculation of the lower curve of the Bollinger Bands 
    df['Upper_Bollinger'] = df['SMA'] + (2 * df['stdev'])   #Upper curve

    df['TR'] = abs(df['High'] - df['Low'])      #True Range calculation
    df['ATR'] = df['TR'].rolling(window = 20).mean()    #Average True Range

    df['Upper_KC'] = df['SMA'] + (1.2 * df['ATR'])      #Upper curve of the Keltner Channel
    df['Lower_KC'] = df['SMA'] - (1.2 * df['ATR'])      #Lower curve

    def in_consolidation(df):       #function testing if a symbol is consolidating (Bollinger Bands in Keltner Channel)
        return df['Lower_Bollinger'] > df['Lower_KC'] and df['Upper_Bollinger'] < df['Upper_KC']

    df['consolidation'] = df.apply(in_consolidation, axis = 1)

    if df.iloc[-1]['consolidation']:
        print("{} is in consolidation".format(symbol))

    if df.iloc[-3]['consolidation'] and not df.iloc[-1]['consolidation']:
        print("{} is coming out of consolidation".format(symbol))

