import os
import yfinance as yf

with open("symbols/S&P500.csv") as f:
    symbols = f.read().splitlines()
    for symbol in symbols:
        data = yf.download(symbol, start="2020-05-01", end="2020-09-03")
        data.to_csv("datasets/S&P500/{}.csv".format(symbol))