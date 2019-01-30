#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona

from abc import ABC, ABCMeta, abstractmethod
from tkinter import CENTER, RIGHT, E, Entry, Message, N, S, StringVar, Toplevel, W, BROWSE
from tkinter.ttk import Button, Combobox, Entry, Label, LabelFrame, Style, Treeview


class V_Main(object):
    """Implementacion de la clase MainView encargada del diseño de la ventana principal"""

    def __init__(self, root, controller):
        """root = Referencia a la ventana principal\ncontroller = Referencia al controlador princiapl de la vista"""

        # Guardamos las referencias del root y controller
        self.root = root
        self.root.resizable(width=False, height=False)
        self.controller = controller
        # Elementos  Gui
        self.textReport = StringVar()
        self.textReport.set('Genera un reporte')
        self.animalsList = Treeview(
            self.root, height=15, columns=('type','domestic', 'gender'), selectmode=BROWSE)
        self.reportBox = Message(self.root, width=250,
                                 textvariable=self.textReport)

        # TreeView de los animales
        self.animalsList.heading('#0', text='ID', anchor=CENTER)
        self.animalsList.column('#0', width=100, minwidth=100)
        self.animalsList.heading('type', text='Tipo', anchor=CENTER)
        self.animalsList.column('type', width=100, minwidth=100)
        self.animalsList.heading('domestic', text='Domestico', anchor=CENTER)
        self.animalsList.column('domestic', width=100, minwidth=100)
        self.animalsList.heading('gender', text='Genero', anchor=CENTER)
        self.animalsList.column('gender', width=60, minwidth=60)
        self.animalsList.grid(row=1, column=1, columnspan=3)
        self.animalsList.bind("<Double-1>", self.onDoubleClick)

        # Entry ReportBox
        self.reportBox.grid(row=1, column=5, rowspan=15,
                            columnspan=6, sticky=W+E+N+S)
        self.btnGenerateReport = Button(
            self.root, text='Reporte', command=self.generateReport)
        self.btnGenerateReport.grid(row=16, column=5, columnspan=6, sticky=W+E)

    def generateReport(self):
        self.controller.getReport()
    
    def onDoubleClick(self, event):
        animal = self.animalsList.selection()[0]
        valores = self.animalsList.item(animal, "values")
        print('Doble click: {}'.format(valores[0]))


class WindowNewAnimal(ABC, Toplevel):
    def __init__(self, controller, titulo: str, ancho=0, alto=0, resizable=False):
        __metaclass__ = ABCMeta
        Toplevel.__init__(self)
        self.controller = controller
        self.title(titulo)
        self.resizable(width=resizable, height=resizable)
        self.setGeometry(ancho, alto)
        self.estilos = Style()
        # Variables
        self.aviso = StringVar()
        # Elementos Gui
        self.frameGui = LabelFrame(self, text=titulo)
        self.entryType = Combobox(self.frameGui, state='readonly')
        self.entryDomestic = Combobox(self.frameGui, state='readonly')
        self.entryAge = Entry(self.frameGui)
        self.entryGender = Combobox(self.frameGui, state='readonly')
        self.entryAttitude = Combobox(self.frameGui, state='readonly')
        self.entryCastrated = Combobox(self.frameGui, state='readonly')
        self.btnAceptar = Button(
            self.frameGui, text='Aceptar', command=self.addAnimal)

        self.labelAviso = Label(self.frameGui, textvariable=self.aviso, justify=RIGHT, foreground='red')
        self.setGui()

    def setGeometry(self, ancho, alto):
        if ancho != 0 and alto != 0:
            self.geometry('{}x{}'.format(ancho, alto))

    def setGui(self):
        # Frame general
        self.frameGui.grid(row=0, column=0, columnspan=4, pady=10, padx=5)
        # Combo Type
        Label(self.frameGui, text='Tipo: ').grid(row=1, column=0)
        self.entryType['values'] = ['PERRO', 'GATO', 'AVE', 'TORTUGA']
        self.entryType.grid(row=1, column=1)
        # Combo Domestic
        Label(self.frameGui, text='Domestico: ').grid(row=1, column=2)
        self.entryDomestic.grid(row=1, column=3)
        # Entry Age
        Label(self.frameGui, text='Edad: ').grid(row=2, column=0)
        self.entryAge.grid(row=2, column=1, sticky=W+E)
        # Combo Gender
        Label(self.frameGui, text='Genero: ').grid(row=2, column=2)
        self.entryGender['values'] = ['F', 'M']
        self.entryGender.grid(row=2, column=3)
        # Combo Attitude
        Label(self.frameGui, text='Actitud: ').grid(row=3, column=0)
        self.entryAttitude['values'] = ['DOCIL', 'AGRESIVO']
        self.entryAttitude.grid(row=3, column=1)
        # Combo Castrated
        Label(self.frameGui, text='Castrado: ').grid(row=3, column=2)
        self.entryCastrated['values'] = ['True', 'False']
        self.entryCastrated.grid(row=3, column=3)

    @abstractmethod
    def addAnimal(self):
        pass


class WindowNewDomesticAnimal(WindowNewAnimal):
    def __init__(self, controller, titulo: str, ancho=0, alto=0, resizable=False):
        super().__init__(controller, titulo, ancho=ancho, alto=alto, resizable=resizable)
        self.entryResidentialArea = Entry(self.frameGui)
        self.entryOwnerName = Entry(self.frameGui)
        self.entryVaccinations = Combobox(self.frameGui, state='readonly')

        # Config Extra Entry's
        # Entry Domestic
        self.entryDomestic['values'] = ['True']
        self.entryDomestic.set('True')
        # Entry ResidentialArea
        Label(self.frameGui, text='Zona: ').grid(row=4, column=0)
        self.entryResidentialArea.grid(row=4, column=1, sticky=W+E)
        # Combo OwnerName
        Label(self.frameGui, text='Dueño: ').grid(row=4, column=2)
        self.entryOwnerName.grid(row=4, column=3, sticky=W+E)
        # Combo Vaccinations
        Label(self.frameGui, text='Vacunas: ').grid(row=5, column=0)
        self.entryVaccinations['values'] = ['True', 'False']
        self.entryVaccinations.grid(row=5, column=1)
        # Label Aviso
        self.labelAviso.grid(row=6, column = 0, columnspan=4, sticky=W+E)
        # Button Aceptar
        self.btnAceptar.grid(row=7, column=0, columnspan=4, sticky=W+E)

    def addAnimal(self):
        self.controller.addAnimal(True)


class WindowNewStreetAnimal(WindowNewAnimal):
    def __init__(self, controller, titulo: str, ancho=0, alto=0, resizable=False):
        super().__init__(controller, titulo, ancho=ancho, alto=alto, resizable=resizable)
        self.entryFoundArea = Entry(self.frameGui)
        self.entryFindingName = Entry(self.frameGui)

        # Config Extra Entry's
        # Entry Domestic
        self.entryDomestic['values'] = ['False']
        self.entryDomestic.set('False')
        # Entry ResidentialArea
        Label(self.frameGui, text='Zona: ').grid(row=4, column=0)
        self.entryFoundArea.grid(row=4, column=1, sticky=W+E)
        # Combo OwnerName
        Label(self.frameGui, text='Responsable: ').grid(row=4, column=2)
        self.entryFindingName.grid(row=4, column=3, sticky=W+E)
        # Label Aviso
        self.labelAviso.grid(row=5, column = 0, columnspan=4, sticky=W+E)
        # Button Aceptar
        self.btnAceptar.grid(row=6, column=0, columnspan=4, sticky=W+E)

    def addAnimal(self):
        self.controller.addAnimal(False)
