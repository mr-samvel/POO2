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
            highs.append(int(float(value[1][1])))
            lows.append(int(float(value[2][1])))
            closes.append(int(float(value[3][1])))
            volumes.append(int(float(value[4][1])))
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
            for j in range(0, 5):
                m += ( highs[i+j] + lows[i+j] ) / 2
            media.append(m/5)
        return media
    
    def __filterArrays(self, *args):
        for arg in args:
            del(arg[0 : (len(arg)-80) ])
        return args

    def __plotGraph(self, nome, tempos, opens, highs, lows, closes, volumes):
        tempos, opens, highs, lows, closes, volumes = self.__reverseArrays(tempos, opens, highs, lows, closes, volumes)
        mediaMovel = self.__calcMediaMovel(highs, lows)
        tempos, opens, highs, lows, closes, volumes, mediaMovel = self.__filterArrays(tempos, opens, highs, lows, closes, volumes, mediaMovel)
        
        fig, ax = plt.subplots()

        candle = []
        for k in range(len(tempos)):
            candle.append((tempos[k], opens[k], highs[k], lows[k], closes[k]))
        mpl_finance.candlestick_ohlc(ax, candle, width=1, colorup='g', colordown='r', alpha=1.0)

        ax.plot(tempos, mediaMovel)
        ax.set(xlabel='Timestamp', ylabel='Preço', title=nome)

        plt.show()

    def __analisarAsCurvas(self):
        # TODO
        # esse pass aqui \/ é pra substituir dps com o return 0, 1 ou 2 (que representa a ação que o usuário tem que tomar - comprar, vender etc)
        pass
