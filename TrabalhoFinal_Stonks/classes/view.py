from tkinter import *

class View:
    def __init__(self, stonksPlotter, stonksNames):
        self.__root = Tk()
        self.__stonksPlotter = stonksPlotter
        self.__stonksNames = stonksNames
        self.__height = 400
        self.__width = 500
    
    ### Funções para criar elementos
    def __createFrame(self, root):
        frame = Frame(root, height=self.__height, width=self.__width)
        frame.pack(fill=X, expand=True)
        frame.pack_propagate(0)
        return frame

    def __createTitle(self, frame, text, padding):
        title = Label(frame, text=text, font=('Helvetica', 18))
        title.pack(pady=padding, side=TOP)
        return title

    def __createLabel(self, frame, text, padding):
        label = Label(frame, text=text, font=('Helvetica', 13))
        label.pack(pady=padding, side=TOP)
        return label

    def __createInput(self, frame, stringvar, padding, isPassword=False):
        input = Entry(frame, textvariable=StringVar(value=stringvar), width=50, show='*' if isPassword else '')
        input.pack(ipady=3, pady=padding, side=TOP)
        return input
    
    # Criar esse wrapper aqui foi chato, porque quando chamava essa funcao passando o callback com algum argumento,
    # o callback era chamado já na criacao do botao. Até que eu descobri essa maravilha desse *
    def __createButton(self, frame, txt, padding, paddingSide, handler, *args):
        btn = Button(frame, text=txt, command=lambda:handler(*args))
        btn.pack(pady=padding, side=paddingSide)
        return btn

    
    ### Frame principal
    def mainFrame(self):
        self.__buttons = []
        mainFrame = self.__createFrame(self.__root)
        self.__mainFrame = mainFrame
        t = self.__createTitle(mainFrame, 'Trabalho Final', 10)
        l = self.__createLabel(mainFrame, 'Sistema de alerta de compra e venda de ativos financeiros', 1)
        for stonk in self.__stonksNames:
            if self.__stonksNames[0] == stonk:  # Esse if é só pra ajeitar o padding
                self.__buttons.append(self.__createButton(mainFrame, stonk, (20, 5), TOP, self.__callPlotter, stonk))
            else:
                self.__buttons.append(self.__createButton(mainFrame, stonk, 5, TOP, self.__callPlotter, stonk))
        if len(self.__stonksNames) < 7:
            add = self.__createButton(mainFrame, 'Adicionar Outra Ação', (0, 15), BOTTOM, self.addAnotherStonkForm)
        mainFrame.tkraise()

    ### Formulario p/ adicionar outra acao
    def addAnotherStonkForm(self):
        form = Toplevel(self.__root)
        formFrame = self.__createFrame(form)
        nomeLabel = self.__createLabel(formFrame, 'Código da ação:', 10)
        nomeInput = self.__createInput(formFrame, 'ex.: XMR', 3)
        urlLabel = self.__createLabel(formFrame, 'URL p/ request:', 10)
        urlInput = self.__createInput(formFrame, 'ex.: https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=XMR&market=CNY&apikey=QO7KBACPTDT2LZ4F', 3)
        submitBtn = self.__createButton(formFrame, 'Ok', 30, BOTTOM, self.__addAnotherStonk, form, nomeInput, urlInput)
        formFrame.tkraise()
    
    ### Handler dos botões
    def __callPlotter(self, stonk):
        # TODO: Essa função chama a plotagem da stonk
        action = self.__stonksPlotter.plotStonk(stonk)
        # TODO: action é 0, 1 ou 2 mostrar alerta pra cada caso.

    def __addAnotherStonk(self, form, nomeInput, urlInput):
        nome = nomeInput.get()
        url = urlInput.get()
        self.__stonksNames.append(nome)
        self.__stonksPlotter.addStonkToFile(nome, url)
        self.__mainFrame.pack_forget()
        self.__mainFrame.destroy()
        self.mainFrame()
        form.destroy()
    
    def run(self):
        self.__root.mainloop()
        