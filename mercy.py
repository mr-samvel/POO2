import json
import numpy as np
import matplotlib as mpl
from datetime import date
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.pyplot as plt
import datetime
import urllib.request

class Plot:
    def __init__(self, file):
        self.__file = file
        self.__tempot = []
        self.__openst = []
        self.__highst = []
        self.__lowt = []
        self.__closest = []
        self.__volumet = []
        self.__datast =[]
        self.__timet = []
        self.__mediam = []
        self.__timet = []
        self.__name = []
        self.readAndPlotJSON()

    def get_file(self):
        return self.__file[0]

    def readAndPlotJSON(self):
        data = json.loads(self.get_file.decode('utf-8'))
        self.__name = data['Meta Data']['2. Digital Currency Code']
        self.__timet = data['Time Series (Digital Currency Daily)']
        
        tempo = [i for i, v in data['Time Series (Digital Currency Daily)'].items()]
        for key, value in timeSeries.items():
            self.__openst.append(float(value['1a. open (CNY)']))
            self.__highst.append(float(value['2a. high (CNY)']))
            self.__lowt.append(float(value['3a. low (CNY)']))
            self.__closest.append(float(value['4a. close (CNY)']))
            self.__volumet.append(float(value['5. volume']))
        self.__tempot = [mdates.date2num(date(int(data[0:4]), int(data[5:7]), int(data[8:10]))) for data in tempo]

        self.__tempot.reverse()
        self.__openst.reverse()
        self.__highst.reverse()
        self.__lowt.reverse()
        self.__closest.reverse()
        self.__volumet.reverse()
        
        self.__openst = [int(float(i)) for i in self.__openst]
        self.__highst = [int(float(i)) for i in self.__highst]
        self.__lowt = [int(float(i)) for i in self.__lowt]
        self.__closest = [int(float(i)) for i in self.__closest]

        filters()

    # Cria a média móvel e passa pra o vetor "mediam"
    # Como detalhe desta função, o len(mediam) é sempre menor que o len(qualquer_outro_vetor)
    # Fazendo-se necessário portanto, limitar todas os vetores
    def filters(self):
        vett = []
        for i in range(len(self.__highst)-10):
            vett.append(((self.__highst[i]+self.__lowt[i])/2+(self.__highst[i+1]+self.__lowt[i+1])/2+(self.__highst[i+2]+self.__lowt[i+2])/2+(self.__highst[i+3]+self.__lowt[i+3])/2+(self.__highst[i+4]+self.__lowt[i+4])/2)/5)
        self.__mediam.append(vett)

        filt()

    # Limita o tamanho das funções para tornar mais visível as mesmas, e deixar todas do mesmo tamanho de mediam
    # Pode-se alterar o valor "-200" para deixar o gráfico maior ou menor
    # O máximo é 400, já que as vezes o len(de_alguns_vetores) é de apenas 460
    def filt():
        del(self.__tempot[0:((len(self.__tempot)-200))])
        del(self.__openst[0:((len(self.__openst)-200))])
        del(self.__highst[0:((len(self.__highst)-200))])
        del(self.__lowt[0:((len(self.__lowt)-200))])
        del(self.__closest[0:((len(self.__closest)-200))])
        del(self.__volumet[0:((len(self.__volumet)-200))])
        del(self.__mediam[0:((len(self.__mediam)-200))])

        plot_tot()

    #Plota um gráfico dependendo do cout, onde cout vai de 0 à 3(BTC, ETH, XRP, EOS)
    def plot_tot(self):
        fig = plt.figure()
        ax1 = plt.subplot2grid((1,1), (0,0))

        # Tupla necessária para a criação do candle_stick segundo a documentação do Matplotlib
        tup= []
        for el in range(len(self.__tempot)):
            tup.append(tuple ([self.__tempot[el], self.__openst[el], self.__highst[el], self.__lowt[el], self.__closest[el],]))
        mpl_finance.candlestick_ohlc(ax1, tup, width=0.2, colorup='g', colordown='r', alpha=1.0)
        # Plotagem da média móvel
        ax1.plot(self.__tempot, self.__mediam, 'r--', alpha=0.75)
        ax1.xaxis_date()
        ax1.set_title(self.__mediam)
        plt.show()
    

def requestStonks(url):
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req).read()

stonks = []
stonks.append(requestStonks('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=CNY&apikey=demo'))

A = Plot(stonks[0])