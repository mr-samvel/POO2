import json
import matplotlib.pyplot as plt
import datetime
import urllib.request

def requestStonks(url):
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req)

def readAndPlotJSON(file):
    f = open(file, 'r')
    data = json.load(f)
    f.close()

    tempo = []
    opens = []
    highs = []
    closes = []
    name = data['Meta Data']['2. Symbol']
    timeSeries = data['Time Series (Daily)']

    for key, value in timeSeries.items():
        tempo.append(datetime.datetime.strptime(key, '%Y-%m-%d'))
        opens.append(float(value['1. open']))
        highs.append(float(value['2. high']))
        closes.append(float(value['4. close']))

    tempo.reverse()
    opens.reverse()
    highs.reverse()
    closes.reverse()

    plotGraph(name, tempo, opens, 'Open')
    plotGraph(name, tempo, highs, 'High')
    plotGraph(name, tempo, closes, 'Close')

def plotGraph(title, x, y, label):
    x2, y2 = zip(*sorted(zip(x,y),key=lambda x: x[0]))
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Precos')
    plt.plot(x2, y2, label=label)
    plt.legend()

def showGraph():
    plt.show()

# Main
# TODO: PEGAR URLS PARA FAZER REQUEST
# URL1 = 'https://alphavantage.com/dasygfsauydfa'
stonks = []
stonks.append(requestStonks(URL1))
stonks.append(requestStonks(URL2))
stonks.append(requestStonks(URL3))
stonks.append(requestStonks(URL4))

plt.subplot(2, 2, 1)
readAndPlotJSON(stonks[0])
plt.subplot(2, 2, 2)
readAndPlotJSON(stonks[1])
plt.subplot(2, 2, 3)
readAndPlotJSON(stonks[2])
plt.subplot(2, 2, 4)
readAndPlotJSON(stonks[3])
showGraph()
