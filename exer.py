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

tempot = []
openst = []
highst = []
lowt = []
closest = []
volumet = []
datast =[]
namet = []
timet = []

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
    
    opens = [int(float(i)) for i in opens]
    highs = [int(float(i)) for i in highs]
    low = [int(float(i)) for i in low]
    closes = [int(float(i)) for i in closes]
    
    tempot.append(tempoc)
    openst.append(opens)
    highst.append(highs)
    lowt.append(low)
    closest.append(closes)
    volumet.append(volume)
    datast.append(datas)
    namet.append(name)
    timet.append(timeSeries)

def plot_tot(name, tempoc, opens, highs, low, closes, volume):

    cout = 0
    fig, ax = plt.subplots(2, 2)
    fig.patch.set_facecolor('xkcd:gray')
    for i in range(0, 2):
        for j in range(0, 2):
            tup= []
            for el in range(len(tempoc[cout])):
                tup.append(tuple ([tempoc[cout][el], opens[cout][el], highs[cout][el], low[cout][el], closes[cout][el],]))
            mpl_finance.candlestick_ohlc(ax[i][j], tup, width=0.2, colorup='g', colordown='r', alpha=1.0)
            #ax[i][j].bar(tempoc[cout], volume[cout]) #volume muito alto
            '''plt.title(name[cout])
            plt.xlabel('Date')
            plt.ylabel('Value')'''
            ax[i][j].xaxis_date()
            ax[i][j].set_title(name[cout])
            for l in ax[i, j].get_xticklabels():
                l.set_rotation(20)
            for l in ax[j, i].get_xticklabels():
                l.set_rotation(20)
            cout = cout + 1
    
    plt.show()

# Main
stonks = []
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=CNY&apikey=demo'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=ETH&market=CNY&apikey=QO7KBACPTDT2LZ4F'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=XRP&market=CNY&apikey=QO7KBACPTDT2LZ4F'))
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=EOS&market=CNY&apikey=QO7KBACPTDT2LZ4F'))

readAndPlotJSON(stonks[0])
readAndPlotJSON(stonks[1])
readAndPlotJSON(stonks[2])
readAndPlotJSON(stonks[3])
plot_tot(namet, tempot, openst, highst, lowt, closest, volumet)

plt.show()