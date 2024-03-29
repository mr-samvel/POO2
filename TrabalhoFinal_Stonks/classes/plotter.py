import json
import urllib.request
from datetime import date
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.widgets as mwidg
import mpl_finance
from classes.view import View

class StonksPlotter:
    def __init__(self, stonks):
        self.__stonks = stonks

    ### Para armazenamento e leitura de dados.
    # Essa função escreve no arquivo com os nomes e urls
    def addStonkToFile(self, name, url):
        obj = {name: url}
        with open('stonks.json', 'r+') as stonks:
            data = json.load(stonks)
            data.update(obj)
            stonks.seek(0)
            json.dump(data, stonks, indent=4)

    # E essa, como deve ter percebido, lê os nomes desse mesmo arquivo
    def getStonksNames(self):
        names = []
        for key in self.__stonks:
            names.append(key)
        return names

    # É necessário sempre chamar essa função p/ ler a tabela de stonks.json, porque ela pode ser atualizada
    # portanto essa função atualiza self.__stonks
    def __readJSON(self):
        with open('stonks.json') as stonksFile:
            self.__stonks = json.load(stonksFile)
        stonksFile.close()

    # Essa função faz o request do arquivo na url e o retorna como File
    def __requestStonks(self, url):
        req = urllib.request.Request(url)
        return urllib.request.urlopen(req).read()

  
    ### Tratamento dos arrays
    # Essa função apenas inverte a ordem dos índices do array
    def __reverseArrays(self, *args):
        for arg in args:
            arg.reverse()
        return args

    # Essa função calcula e retorna um vetor com a media movel com peso "peso"
    def __calcMediaMovel(self, highs, lows, peso):
        media = []
        for i in range(len(highs)-peso+1):
            m = 0
            for j in range(0, peso):
                m += ( highs[i+j] + lows[i+j] ) / 2
            media.append(m/peso)
        return media

    # Para tornar os gráficos mais legíveis, delimita-se a quantidade de informações
    # contidas no mesmo. Nesse caso, os vetores permanecem com apenas 150 dados mais recentes
    def __filterArrays(self, *args):
        for arg in args:
            del(arg[0 : (len(arg)-150) ])
        return args


    ### Plotagem
    # Função responsável por fazer o request, montar os vetores e chamar a função p/ plotar
    def plotStonk(self, stonkName):
        self.__readJSON()
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
        #Transforma a data em um número
        tempos = [mdates.date2num(date(int(data[0:4]), int(data[5:7]), int(data[8:10]))) for data in tempos]

        # Tratamento dos vetores
        tempos, opens, highs, lows, closes, volumes = self.__reverseArrays(tempos, opens, highs, lows, closes, volumes)
        mediaMovel = self.__calcMediaMovel(highs, lows, 9)
        mediaMovelQ = self.__calcMediaMovel(highs, lows, 40)
        tempos, opens, highs, lows, closes, volumes, mediaMovel, mediaMovelQ = self.__filterArrays(tempos, opens, highs, lows, closes, volumes, mediaMovel, mediaMovelQ)

        self.__plotGraph(name, tempos, opens, highs, lows, closes, volumes, mediaMovel, mediaMovelQ)

    def __plotGraph(self, nome, tempos, opens, highs, lows, closes, volumes, mediaMovel, mediaMovelQ):
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)

        # Criar e plotar candlestick
        candle = []
        for k in range(len(tempos)):
            candle.append((tempos[k], opens[k], highs[k], lows[k], closes[k]))
        mpl_finance.candlestick_ohlc(ax, candle, width=0.2, colorup='g', colordown='r', alpha=1.0)

        # Plotagem de ambas as médias móveis
        ax.plot(tempos, mediaMovel, 'b--', alpha=0.75, label='Média Móvel - 9')
        ax.plot(tempos, mediaMovelQ, 'y--', alpha=1, label='Média Móvel - 40')

        # Deficição das labels de eixo
        ax.set(xlabel='Timestamp', ylabel='Preço', title=nome)
        ax.xaxis_date()
        
        # Como no gráfico são dispostos muitos dias, ele acabava ficando poluido e embaraçado
        # com tantas datas, por isso foi usada a função abaixo, que gira as labels do eixo x
        for l in ax.get_xticklabels():
            l.set_rotation(20)

        # Mostrar legendas
        plt.legend()

        # Analise das medias moveis
        action = self.__analisarAsCurvas(mediaMovel, mediaMovelQ)

        # Botão para chamar a caixa de texto que avisa a ação que o usuário deve tomar
        btnAx = plt.axes([0.7, 0.03, 0.2, 0.075])
        actionBtn = mwidg.Button(btnAx, 'Recomendação')
        actionBtn.on_clicked(lambda event: View.callMessageBoxToAction(action, nome, event))

        plt.show()
    
    # Método que retornar qual operação deve ser realizada com base em uma analise de dados
    # de Médias Móveis 9:40
    def __analisarAsCurvas(self, media, mediaq):
        index = len(media) - 1
        if media[index] > mediaq[index]:
            return 0 #Vender
        elif media[index] < mediaq[index]:
            return 1 #Comprar

        return 2 #Esperar