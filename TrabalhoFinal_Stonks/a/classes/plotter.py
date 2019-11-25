import json
import urllib.request

class StonksPlotter:
    def __init__(self, stonks):
        self.__stonks = stonks
        self.__requestStonks(stonks)

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
        
        data = json.load(f.decode('utf-8'))
        
        # e daqui vai, essa função deve plottar o grafico

        return self.analisarAsCurvas()
    
    def analisarAsCurvas(self):
        # e daqui vai pt. 2
        # esse pass aqui \/ é pra substituir dps com o return 0, 1 ou 2 (que representa a ação que o usuário tem que tomar - comprar, vender etc)
        pass
