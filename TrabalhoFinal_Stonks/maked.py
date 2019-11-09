import json
import numpy as np
import matplotlib as mpl
from datetime import date
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.pyplot as plt
import datetime
import urllib.request

#BTC, ETH, XRP, EOS

def requestStonks(url):
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req).read()

def readAndPlotJSON(file, x):
    data = json.loads(file.decode('utf-8'))

    tempo = []
    opens = []
    highs = []
    low = []
    closes = []
    volume = []
    datas = []
    name = data['Meta Data']['2. Digital Currency Code']
    timeSeries = data['Time Series (Digital Currency Daily)']
    
    tempo = [i for i, v in data['Time Series (Digital Currency Daily)'].items()]
    for key, value in timeSeries.items():
        opens.append(float(value['1a. open (CNY)']))
        highs.append(float(value['2a. high (CNY)']))
        low.append(float(value['3a. low (CNY)']))
        closes.append(float(value['4a. close (CNY)']))
        volume.append(float(value['5. volume']))
    tempoc = [mdates.date2num(date(int(data[0:4]), int(data[5:7]), int(data[8:10]))) for data in tempo]

    tempoc.reverse()
    opens.reverse()
    highs.reverse()
    low.reverse()
    closes.reverse()
    volume.reverse()

    plot_tot(name, tempoc, opens, highs, low, closes, volume, x)

def plot_tot(name, tempoc, opens, highs, low, closes, volume, x):
    opens = [int(float(i)) for i in opens]
    highs = [int(float(i)) for i in highs]
    low = [int(float(i)) for i in low]
    closes = [int(float(i)) for i in closes]
    
    fig, ax = plt.subplots(figsize = (10,5))
    tup= []
    for i in range(len(tempoc)):
        tup.append(tuple ([tempoc[i], opens[i], highs[i], low[i], closes[i],]))
    mpl_finance.candlestick_ohlc(ax, tup, width=0.2, colorup='g', colordown='r', alpha=1.0)
    #plt.bar(tempoc, volume, label = "Volume") #volume muito alto
    ax.xaxis_date()
    plt.xticks(rotation=20)
    plt.title(name)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()

# Main
stonks = []
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=CNY&apikey=demo'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=ETH&market=CNY&apikey=QO7KBACPTDT2LZ4F'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=XRP&market=CNY&apikey=QO7KBACPTDT2LZ4F'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=EOS&market=CNY&apikey=QO7KBACPTDT2LZ4F'))

readAndPlotJSON(stonks[0], 1)
readAndPlotJSON(stonks[1], 2)
readAndPlotJSON(stonks[2], 3)
readAndPlotJSON(stonks[3], 4)
plt.show()
