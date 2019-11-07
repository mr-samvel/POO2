import json
import numpy as np
import matplotlib as mpl
from datetime import date
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.pyplot as plt
import datetime
import urllib.request

def requestStonks(url):
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req).read()

def readAndPlotJSON(file):
    data = json.loads(file.decode('utf-8'))

    tempo = []
    opens = []
    highs = []
    low = []
    closes = []
    volume = []
    datas = []
    name = data['Meta Data']['2. Symbol']
    timeSeries = data['Time Series (Daily)']
    
    tempo = [i for i, v in data['Time Series (Daily)'].items()]
    for key, value in timeSeries.items():
        opens.append(float(value['1. open']))
        highs.append(float(value['2. high']))
        low.append(float(value['3. low']))
        closes.append(float(value['4. close']))
        volume.append(float(value['5. volume']))
    tempoc = [mdates.date2num(date(int(data[0:4]), int(data[5:7]), int(data[8:10]))) for data in tempo]

    tempoc.reverse()
    opens.reverse()
    highs.reverse()
    low.reverse()
    closes.reverse()
    volume.reverse()

    plot_tot(name, tempoc, opens, highs, low, closes, volume)

def plot_tot(name, tempoc, opens, highs, low, closes, volume):
    opens = [int(float(i)) for i in opens]
    highs = [int(float(i)) for i in highs]
    low = [int(float(i)) for i in low]
    closes = [int(float(i)) for i in closes]
    
    figure, ax = plt.subplots(figsize = (10,5))
    tup= []
    for i in range(len(tempoc)):
        tup.append(tuple ([tempoc[i], opens[i], highs[i], low[i], closes[i],]))
    mpl_finance.candlestick_ohlc(ax, tup, colordown='r', colorup='g')
    ax.plot(tempoc, volume, 'b', alpha=0.5, label = "Volume")
    
    ax.xaxis_date()
    plt.xticks(rotation=20)
    plt.title(name)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()

def showGraph():
    plt.show()

# Main
stonks = []
stonks.append(requestStonks('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=seila'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=seila'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOGL&apikey=seila'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=VALE&apikey=seila'))

plt.subplot(2, 2, 1)
readAndPlotJSON(stonks[0])
plt.subplot(2, 2, 2)
readAndPlotJSON(stonks[1])
plt.subplot(2, 2, 3)
readAndPlotJSON(stonks[2])
plt.subplot(2, 2, 4)
readAndPlotJSON(stonks[3])
showGraph()
