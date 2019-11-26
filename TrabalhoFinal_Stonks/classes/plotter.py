import json
import urllib.request
from datetime import date
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mpl_finance

class StonksPlotter:
    def __init__(self, stonks):
        self.__stonks = stonks

    ### Para armazenamento e leitura de dados.
    def addStonkToFile(self, name, url):
        obj = {name: url}
        with open('stonks.json', 'r+') as stonks:
            data = json.load(stonks)
            data.update(obj)
            stonks.seek(0)
            json.dump(data, stonks, indent=4)

    def getStonksNames(self):
        names = []
        for key in self.__stonks:
            names.append(key)
        return names

    # É necessário sempre chamar essa função p/ ler a tabela de stonks.json, porque ela pode ser atualizada
    # portanto essa função atualiza self.__stonks
    def readJSON(self):
        with open('stonks.json') as stonksFile:
            self.__stonks = json.load(stonksFile)
        stonksFile.close()

    def __requestStonks(self, url):
        req = urllib.request.Request(url)
        return urllib.request.urlopen(req).read()

    ### Plotagem
    def plotStonk(self, stonkName):
        self.readJSON()
        url = self.__stonks[stonkName]
        f = self.__requestStonks(url)

        data = json.loads(f.decode('utf-8'))

        tempos = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []

        # meu deus do ceu eu odeio python
        listItems = list(data.items())
        name = list(listItems[0][1].values())[1]
        timeSeries = listItems[1][1] # tupla ( 'time series', obj{} )

        for key, value in timeSeries.items():
            # key: YYYY-MM-DD
            # value: {key: value}
            value = list(value.items())
            tempos.append(key)
            opens.append(int(float(value[0][1])))
            highs.append(int(float(value[2][1])))
            lows.append(int(float(value[4][1])))
            closes.append(int(float(value[6][1])))
            volumes.append(int(float(value[8][1])))
        tempos = [mdates.date2num(date(int(data[0:4]), int(data[5:7]), int(data[8:10]))) for data in tempos]

        self.__plotGraph(name, tempos, opens, highs, lows, closes, volumes)
        # return self.__analisarAsCurvas()


    def __reverseArrays(self, *args):
        for arg in args:
            arg.reverse()
        return args

    # Essa função calcula e retorna um vetor com a media movel
    def __calcMediaMovel(self, highs, lows):
        media = []
        for i in range(len(highs)-10):
            m = 0
            for j in range(0, 9):
                m += ( highs[i+j] + lows[i+j] ) / 2
            media.append(m/9)
        return media

    def __calcMediaMovelQ(self, highs, lows):
        media = []
        for i in range(len(highs)-41):
            m = 0
            for j in range(0, 40):
                m += ( highs[i+j] + lows[i+j] ) / 2
            media.append(m/40)
        return media

    def __filterArrays(self, *args):
        for arg in args:
            del(arg[0 : (len(arg)-150) ])
        return args

    def __plotGraph(self, nome, tempos, opens, highs, lows, closes, volumes):
        tempos, opens, highs, lows, closes, volumes = self.__reverseArrays(tempos, opens, highs, lows, closes, volumes)
        mediaMovel = self.__calcMediaMovel(highs, lows)
        mediaMovelQ = self.__calcMediaMovelQ(highs, lows)
        tempos, opens, highs, lows, closes, volumes, mediaMovel, mediaMovelQ = self.__filterArrays(tempos, opens, highs, lows, closes, volumes, mediaMovel, mediaMovelQ)

        fig, ax = plt.subplots()

        candle = []
        for k in range(len(tempos)):
            candle.append((tempos[k], opens[k], highs[k], lows[k], closes[k]))
        mpl_finance.candlestick_ohlc(ax, candle, width=0.2, colorup='g', colordown='r', alpha=1.0)

        ax.plot(tempos, mediaMovel, 'b--', alpha=0.75, label='Média Móvel - 9')
        ax.plot(tempos, mediaMovelQ, 'y--', alpha=1, label='Média Móvel - 40')
        ax.set(xlabel='Timestamp', ylabel='Preço', title=nome)
        ax.xaxis_date()
        for l in ax.get_xticklabels():
            l.set_rotation(20)

        plt.legend()
        plt.show()

    def __analisarAsCurvas(self, media, mediaq):
        if media[len(media)] > mediaq[len(media)]:
            return 0 #Vender
        elif media[len(media)] < mediaq[len(media)]:
            return 1 #Comprar
        else:
            return 2 #Esperar