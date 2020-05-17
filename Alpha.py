import requests
import pandas as pd
import json

def getMinInterval(ticker, showTable=False):
    keys = json.load(open('keys.json'))

    # Basic collection of stock data
    interval = '1min'
    url = ('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + ticker + 
            '&interval='+interval+
            '&outputsize=full&apikey='+keys['alpha'])

    r = requests.get(url)
    result = r.json()
    dataForAllDays = result['Time Series (' + interval + ')']
    #convert to dataframe
    df = pd.DataFrame.from_dict(dataForAllDays, orient='index') 
    df = df.reset_index()

    #rename columns
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})

    #Changing to datetime
    df['date'] = pd.to_datetime(df['date'])

    #Sort according to date
    df = df.sort_values(by=['date'])

    #Changing the datatype 
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(int)

    #check the data
    if(showTable):
        print(ticker)
        print(df.head())
        print()

    return df

def getDayInterval(ticker, showTable=False):
    keys = json.load(open('keys.json'))

    # Basic collection of stock data
    url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + 
            '&outputsize=full&apikey='+keys['alpha'])

    r = requests.get(url)
    result = r.json()
    dataForAllDays = result['Time Series (Daily)']
    #convert to dataframe
    df = pd.DataFrame.from_dict(dataForAllDays, orient='index') 
    df = df.reset_index()

    #rename columns
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})

    #Changing to datetime
    df['date'] = pd.to_datetime(df['date'])

    #Sort according to date
    df = df.sort_values(by=['date'])

    #Changing the datatype 
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(int)

    # CHECK DATA
    if(showTable):
        print(ticker)
        print(df.head())
        print()

    return df