#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona

from tkinter import END, Toplevel, Tk

from src.view import V_Main, WindowNewDomesticAnimal, WindowNewStreetAnimal
from src.dataController import Data
from src.model import DomesticAnimalList, StreetAnimalList


class C_Main(object):
    """Implementacion de la clase C_Main encargada de las operaciones principales"""

    def __init__(self, root: Tk):
        """root = Referencia a la ventana principal"""
        self.root = V_Main(root, self)
        self.windowDomestic = WindowNewDomesticAnimal(self, 'Nuevo domestico')
        self.windowStreet = WindowNewStreetAnimal(self, 'Nuevo Callejero')
        self.data = Data('data.csv', ',', 'data.csv')
        self.domesticAnimalList = DomesticAnimalList('Domesticos',
                                                     self.data.getData('domestic', 'True'))
        self.streetAnimalList = StreetAnimalList('Callejeros',
                                                 self.data.getData('domestic', 'False'))
        self.animalsList = [self.domesticAnimalList, self.streetAnimalList]
        self.animalsListFull = self.reloadListFull()
        # print(self.domesticAnimalList)
        self.getAnimals()
        self.lastId = self.maxId()

    def maxId(self):
        return max(self.domesticAnimalList.lastId, self.streetAnimalList.lastId)

    def reloadListFull(self):
        listFull = []
        for listAnimals in self.animalsList:
            for animal in listAnimals.animals:
                listFull.append(animal)
        self.bubbleSort(listFull)
        return listFull

    def bubbleSort(self, lista):
        for i in range(len(lista)-1, 0, -1):
            for j in range(i):
                if lista[j].id > lista[j+1].id:
                    temp = lista[j]
                    lista[j] = lista[j+1]
                    lista[j+1] = temp

    def getAnimals(self, asc=True):
        """Metodo que actualiza el TreeView"""
        tree = self.root.animalsList
        records = tree.get_children()
        for record in records:
            tree.delete(record)
            # tree.

        if asc:

            for i in range(len(self.animalsListFull)-1, -1, -1):
                # print(animal.type)
                tree.insert('', 0, text=self.animalsListFull[i].id, values=[
                            self.animalsListFull[i].type, self.animalsListFull[i].domestic, self.animalsListFull[i].gender])
        else:
            for animal in self.animalsListFull:
                # print(animal.type)
                tree.insert('', 0, text=animal.id, values=[
                            animal.type, animal.domestic, animal.gender])

    def addAnimal(self, domestic: bool):
        if domestic:
            ventana = self.windowDomestic
        else:
            ventana = self.windowStreet

        dataType = ventana.entryType.get()
        dataDomestic = ventana.entryDomestic.get()
        dataAge = ventana.entryAge.get()
        dataGender = ventana.entryGender.get()
        dataAttitude = ventana.entryAttitude.get()
        dataCastrated = ventana.entryCastrated.get()

        if dataType == '' or dataDomestic == '' or dataAge == '' or dataGender == '' or dataAttitude == '' or dataCastrated == '':
            self.alert('Llene todos los campos', ventana)
        else:
            try:
                dataAge = int(dataAge)
                correcto = True
            except ValueError as e:
                correcto = False
                self.alert(
                    'Edad incorrecta, escriba un valor numerico entero', ventana)

            if correcto:
                if domestic:
                    dataResidentialArea = ventana.entryResidentialArea.get().upper()
                    dataOwnerName = ventana.entryOwnerName.get().upper()
                    dataVaccinations = ventana.entryVaccinations.get()

                    if dataResidentialArea == '' or dataOwnerName == '' or dataVaccinations == '':
                        self.alert('Llene todos los campos', ventana)
                    else:
                        self.animalsList[0].addAnimal(self.lastId + 1, dataType, dataDomestic, dataAge, dataGender, dataAttitude,
                                                      dataCastrated, dataResidentialArea, dataOwnerName, dataVaccinations)

                        self.clearForm(ventana, domestic)
                        self.lastId += 1
                        print('Add nuevo Domestico')
                else:
                    dataFoundArea = ventana.entryFoundArea.get().upper()
                    dataFindingName = ventana.entryFindingName.get().upper()

                    if dataFoundArea == '' or dataFindingName == '':
                        self.alert('Llene todos los campos', ventana)
                    else:
                        self.animalsList[1].addAnimal(
                            self.lastId + 1, dataType, dataDomestic, dataAge, dataGender, dataAttitude, dataCastrated, dataFoundArea, dataFindingName)

                        self.clearForm(ventana, domestic)
                        self.lastId += 1
                        print('Add nuevo Callejero')

                self.animalsListFull = self.reloadListFull()
                self.getAnimals()
                self.data.writeData(self.animalsListFull)

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

        # print(self.animalsListFull)
        self.data.writeData(self.animalsListFull)

    def alert(self, mensaje: str, ventana: Toplevel):
        ventana.aviso.set(mensaje)

    def clearForm(self, ventana: Toplevel, domestic: bool):
        if domestic:
            ventana.entryResidentialArea.delete(0, END)
            ventana.entryOwnerName.delete(0, END)
            ventana.entryVaccinations.set('')
        else:
            ventana.entryFoundArea.delete(0, END)
            ventana.entryFindingName.delete(0, END)

        ventana.entryType.set('')
        ventana.entryAge.delete(0, END)
        ventana.entryGender.set('')
        ventana.entryAttitude.set('')
        ventana.entryCastrated.set('')
        ventana.aviso.set('')
