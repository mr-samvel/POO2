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
mediam = []

def requestStonks(url):
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req).read()

# Requisição
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

# Cria a média móvel e passa pra o vetor "mediam"
# Como detalhe desta função, o len(mediam) é sempre menor que o len(qualquer_outro_vetor)
# Fazendo-se necessário portanto, limitar todas os vetores
def filters(tempoc, opens, highs, low, closes, volume):
    for key in range(4):
        vett = []
        for i in range(len(low[key])-10):
            vett.append(((highs[key][i]+low[key][i])/2+(highs[key][i+1]+low[key][i+1])/2+(highs[key][i+2]+low[key][i+2])/2+(highs[key][i+3]+low[key][i+3])/2+(highs[key][i+4]+low[key][i+4])/2)/5)
        mediam.append(vett)

# Limita o tamanho das funções para tornar mais visível as mesmas, e deixar todas do mesmo tamanho de mediam
# Pode-se alterar o valor "-200" para deixar o gráfico maior ou menor
# O máximo é 400, já que as vezes o len(de_alguns_vetores) é de apenas 460
def filt():
    for key in range(4):
        del(tempot[key][0:((len(tempot[key])-200))])
        del(openst[key][0:((len(openst[key])-200))])
        del(highst[key][0:((len(highst[key])-200))])
        del(lowt[key][0:((len(lowt[key])-200))])
        del(closest[key][0:((len(closest[key])-200))])
        del(volumet[key][0:((len(volumet[key])-200))])
        del(mediam[key][0:((len(mediam[key])-200))])

#Plota um gráfico dependendo do cout, onde cout vai de 0 à 3(BTC, ETH, XRP, EOS)
def plot_tot(name, tempoc, opens, highs, low, closes, volume, mediam, cout):
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    # Tupla necessária para a criação do candle_stick segundo a documentação do Matplotlib
    tup= []
    for el in range(len(tempoc[cout])):
        tup.append(tuple ([tempoc[cout][el], opens[cout][el], highs[cout][el], low[cout][el], closes[cout][el],]))
    mpl_finance.candlestick_ohlc(ax1, tup, width=0.2, colorup='g', colordown='r', alpha=1.0)
    # Plotagem da média móvel
    ax1.plot(tempoc[cout], mediam[cout], 'r--', alpha=0.75)
    ax1.xaxis_date()
    ax1.set_title(name[cout])
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
filters(tempot, openst, highst, lowt, closest, volumet)
filt()
# Esse plot_tot abaixo, como dito antes, pode ter o valor inteiro alterado para alteração da moeda requisitada
plot_tot(namet, tempot, openst, highst, lowt, closest, volumet, mediam, 0)

plt.show() 
