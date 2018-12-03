#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona

from tkinter import END

from src.view import V_Main, WindowNewDomesticAnimal, WindowNewStreetAnimal
from src.dataController import Data
from src.model import DomesticAnimalList, StreetAnimalList


class C_Main(object):
    """Implementacion de la clase C_Main encargada de las operaciones principales"""

    def __init__(self, root):
        """root = Referencia a la ventana principal"""
        self.root = V_Main(root, self)
        self.windowDomestic = WindowNewDomesticAnimal(self, 'Nuevo domestico')
        self.windowStreet = WindowNewStreetAnimal(self, 'Nuevo Callejero')
        self.data = Data('data.txt', ',', 'dataOut.txt')
        self.domesticAnimalList = DomesticAnimalList('Domesticos',
                                                     self.data.getData('domestic', 'True'))
        self.streetAnimalList = StreetAnimalList('Callejeros',
                                                 self.data.getData('domestic', 'False'))
        self.animalsList = [self.domesticAnimalList, self.streetAnimalList]
        print(self.domesticAnimalList)
        self.getAnimals()

    def getAnimals(self):
        tree = self.root.animalsList
        records = tree.get_children()
        for record in records:
            tree.delete(record)

        for animalList in self.animalsList:
            for animal in animalList.animals:
                # print(animal.type)
                tree.insert('', 0, text=animal.type, values=[
                            animal.domestic, animal.gender])

    def addAnimal(self, domestic):
        if domestic:
            ventana = self.windowDomestic
        else:
            ventana = self.windowStreet

        dataType = ventana.entryType.get()
        dataDomestic = ventana.entryDomestic.get()
        dataAge = int(ventana.entryAge.get())
        dataGender = ventana.entryGender.get()
        dataAttitude = ventana.entryAttitude.get()
        dataCastrated = ventana.entryCastrated.get()

        if domestic:
            dataResidentialArea = ventana.entryResidentialArea.get().upper()
            dataOwnerName = ventana.entryOwnerName.get().upper()
            dataVaccinations = ventana.entryVaccinations.get()
            self.animalsList[0].addAnimal(dataType, dataDomestic, dataAge, dataGender, dataAttitude,
                                          dataCastrated, dataResidentialArea, dataOwnerName, dataVaccinations)
            ventana.entryResidentialArea.delete(0, END)
            ventana.entryOwnerName.delete(0, END)
            ventana.entryVaccinations.set('')
            print('Add nuevo Domestico')
        else:
            dataFoundArea = ventana.entryFoundArea.get().upper()
            dataFindingName = ventana.entryFindingName.get().upper()
            self.animalsList[1].addAnimal(
                dataType, dataDomestic, dataAge, dataGender, dataAttitude, dataCastrated, dataFoundArea, dataFindingName)
            ventana.entryFoundArea.delete(0, END)
            ventana.entryFindingName.delete(0, END)
            print('Add nuevo Callejero')

        ventana.entryType.set('')
        ventana.entryAge.delete(0, END)
        ventana.entryGender.set('')
        ventana.entryAttitude.set('')
        ventana.entryCastrated.set('')

        self.getAnimals()

    def getReport(self):
        numTotals = [0, 0, 0]
        numTotals[0] = len(self.domesticAnimalList.animals)
        numTotals[1] = len(self.streetAnimalList.animals)
        numTotals[2] = numTotals[0] + numTotals[1]
        edadProm = 0
        genero = [0, 0]
        attitude = [0, 0]
        castrated = [0, 0]
        for animalList in self.animalsList:
            for animal in animalList.animals:
                edadProm += animal.age

                if animal.gender == 'M':
                    genero[0] += 1
                else:
                    genero[1] += 1

                if animal.attitude == 'DOCIL':
                    attitude[0] += 1
                else:
                    attitude[1] += 1

                if animal.castrated == True:
                    castrated[0] += 1
                else:
                    castrated[1] += 1

        edadProm = int(edadProm / numTotals[2])
        title = '=== REPORTE GENERAL ==='
        reporte = '{:^30}\n\nNumero Total de Animales: {}\n\tDomesticos: {}\n\tCallejeros: {}\n\nEdad promedio: {} meses\n\nGenero:\n\tFemenino: {}\n\tMasculino: {}\n\nActitud:\n\tDocil: {}\n\tAgresivo: {}\n\nCastrados: Si - {} | No - {}\n'.format(
            title, numTotals[2], numTotals[0], numTotals[1], edadProm, genero[1], genero[0], attitude[0], attitude[1], castrated[0], castrated[1])

        # print(reporte)
        self.root.textReport.set(reporte)
