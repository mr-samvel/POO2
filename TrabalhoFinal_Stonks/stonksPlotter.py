import json
import matplotlib.pyplot as plt
import datetime
import urllib.request

def requestStonks(url):
    print('Fazendo o request da acao no url: ' + url)
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req).read()

def readAndPlotJSON(file):
    data = json.loads(file.decode('utf-8'))

    tempo = []
    opens = []
    highs = []
    closes = []
    name = data['Meta Data']['2. Symbol']
    timeSeries = data['Time Series (Daily)']
    print('Montando o grafico da acao ' + name)
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
print('Iniciando programa')
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
