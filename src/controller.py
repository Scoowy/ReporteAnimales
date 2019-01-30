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
        """Metodo que devuelve el mayor de los ID's de las 2 listas"""
        return max(self.domesticAnimalList.lastId, self.streetAnimalList.lastId)

    def reloadListFull(self):
        """Metodo que unifica las dos listas en una sola"""
        listFull = []
        for listAnimals in self.animalsList:
            for animal in listAnimals.animals:
                listFull.append(animal)
        self.bubbleSort(listFull)
        return listFull

    def bubbleSort(self, lista):
        """Metodo de ordenamiento tipo Burbuja"""
        for i in range(len(lista)-1, 0, -1):
            for j in range(i):
                if lista[j].id > lista[j+1].id:
                    temp = lista[j]
                    lista[j] = lista[j+1]
                    lista[j+1] = temp

    def getAnimals(self, asc=True):
        """Metodo que actualiza el TreeView
        por defecto lo presenta en forma ascendente
        Si se le pasa de argumento False lo presentara
        de forma descendente"""
        tree = self.root.animalsList
        records = tree.get_children()
        for record in records:
            tree.delete(record)
            # tree.

        if asc:
            # Se recorre la lista del final al principio
            for i in range(len(self.animalsListFull)-1, -1, -1):
                # print(animal.type)
                tree.insert('', 0, text=self.animalsListFull[i].id, values=[
                            self.animalsListFull[i].type, self.animalsListFull[i].domestic, self.animalsListFull[i].gender])
        else:
            # Se recorre la lista de forma normal
            for animal in self.animalsListFull:
                # print(animal.type)
                tree.insert('', 0, text=animal.id, values=[
                            animal.type, animal.domestic, animal.gender])

    def addAnimal(self, domestic: bool):
        """Metodo encargado de añadir un nuevo animal domestico determina
        a que grupo de animales perteece"""

        # Segun el tipo se accede alguna de las dos ventanas de formulario
        if domestic:
            ventana = self.windowDomestic
        else:
            ventana = self.windowStreet

        # Se obtienen los datos
        dataType = ventana.entryType.get()
        dataDomestic = ventana.entryDomestic.get()
        dataAge = ventana.entryAge.get()
        dataGender = ventana.entryGender.get()
        dataAttitude = ventana.entryAttitude.get()
        dataCastrated = ventana.entryCastrated.get()

        # Comprobamos si todos los campos etan completos
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

            # Si los datos son correctos los convertimos a un objeto animal
            # de alguno de los dos grupos
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

                # Recargamos la lista completa de animales
                self.animalsListFull = self.reloadListFull()
                # Actualizamos el TreeView
                self.getAnimals()
                # Escribimos los nuevos datos en el archivo CSV
                self.data.writeData(self.animalsListFull)

    def getReport(self):
        """MEtodo que nos muestra un reporte general basico de todos,
        los animales ingresados"""
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

        # Escribimos los resultados en el archivo CSV
        self.data.writeData(self.animalsListFull)

    def alert(self, mensaje: str, ventana: Toplevel):
        """Metodo que actualiza el Label del aviso,
        ventana - Ventana a la cual pertenece el Label"""
        ventana.aviso.set(mensaje)

    def clearForm(self, ventana: Toplevel, domestic: bool):
        """Metodo encargado de resetear o dejar en blanco todo
        el formulario"""
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
