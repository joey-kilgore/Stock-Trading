import pandas as pd

def getSymbols():
    data = pd.read_csv("NYSE.csv")
    symbols = data['ACT Symbol'].to_list()
    newSymbols = []
    for sym in symbols:
        if(sym.find('$') == -1):
            newSymbols.append(sym)

    data = pd.read_csv("NASDAQ.csv")
    symbols = data['Symbol'].to_list()
    for sym in symbols:
        if(sym not in newSymbols):
            newSymbols.append(sym)

    newSymbols.sort()
    return (newSymbols)