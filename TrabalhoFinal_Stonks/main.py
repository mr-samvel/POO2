# Por fins de compatibilidade (windows kkk), adicionando a pasta de classes ao path do Python em runtime
import sys
import os
sys.path.append(os.getcwd() + '\\classes')

# Demais imports
import json
from classes.view import View
from classes.plotter import StonksPlotter

with open('stonks.json') as stonksFile:
    stonks = json.load(stonksFile) # stonks é um dicionario no formato { 'ACAO': { 'URL': 'https://url.com' } }
stonksFile.close()

### Inicialização das classes
stonksPlotter = StonksPlotter(stonks)
view = View(stonksPlotter, stonksPlotter.getStonksNames())

### Programa
view.mainFrame()
view.run()