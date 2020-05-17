import Alpha
import pandas as pd
import datetime

def calculateMovingAverage(ticker, end_date, width, variable="close"):
    df = Alpha.getDayInterval(ticker)

    start_date = end_date - datetime.timedelta(days=width)

    df = df.loc[(df['date'] > start_date) & (df['date'] <= end_date)]

    return df[variable].mean()

def scoreStock(ticker, variable="close"):
    # to score a stock we will look at its 50 day and 150 day moving averages
    fiftyDayAVG = calculateMovingAverage(ticker, datetime.datetime.today(), 20, variable=variable)
    oneFiftyDayAVG = calculateMovingAverage(ticker, datetime.datetime.today(), 150, variable=variable)

    diff = (fiftyDayAVG - oneFiftyDayAVG) / (oneFiftyDayAVG)
    
    # print(variable + " diff : " + str(diff)) # DEBUG CODE

    return diff