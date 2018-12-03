#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona


import os

from src.config import RUTA_BASE
from src.model import DomesticAnimal, StreetAnimal


class Data(object):
    """Clase encargada de gestionar la recuperacion y escritura de datos en los registros de texto"""

    def __init__(self, dataInName: str, separator: str, dataOutName=''):
        self.dataInName = dataInName
        self.dataOutName = dataOutName
        self.separator = separator
        self.dataInPath = self.generatePath(dataInName)
        self.dataOutPath = self.generatePath(dataOutName)
        self.data = self.connectData(self.dataInPath, 'r')

    def setDataOutNamePath(self, dataName: str):
        self.dataOutName = dataName
        self.dataOutPath = self.generatePath(self.dataOutName)

    def generatePath(self, dataName: str):
        return os.path.join(RUTA_BASE, 'data', dataName)

    def connectData(self, dataPath, mode):
        try:
            with open(dataPath, mode) as data:
                return data.readlines()
        except IOError as error:
            print('Algo salio mal')
            print(error)
            return 'ERROR'

    def getData(self, param=None, value=None):
        dataFiltred = []
        if self.data != 'ERROR':
            rows = self.data
            # print(rows)

            if param != None and value != None:

                if param == 'type':
                    col = 0
                elif param == 'domestic':
                    col = 1
                elif param == 'age':
                    col = 2
                elif param == 'gender':
                    col = 3
                elif param == 'attitude':
                    col = 4
                elif param == 'castrated':
                    col = 5

                for row in rows:
                    rowDat = row.split('\n')
                    rowDat = rowDat[0].split(',')
                    # print(rowDat)
                    if rowDat[col] == value:
                        if rowDat[1] == 'True':
                            animal = DomesticAnimal(
                                rowDat[0], self.strToBool(rowDat[1]), int(rowDat[2]), rowDat[3], rowDat[4], self.strToBool(rowDat[5]), rowDat[6], rowDat[7], self.strToBool(rowDat[8]))
                        else:
                            animal = StreetAnimal(
                                rowDat[0], self.strToBool(rowDat[1]), int(rowDat[2]), rowDat[3], rowDat[4], self.strToBool(rowDat[5]), rowDat[6], rowDat[7])
                        # print(animal)
                        dataFiltred.append(animal)
        else:
            print('Error al obtener la informacion')
        return dataFiltred

    def writeData(self, animalsList):
        data = self.connectData(self.dataOutPath, 'w')
        if data != 'ERROR':
            for animal in animalsList:
                data.write(animal)
                print('Archivo escrito')
            else:
                print('ERROR al escribir el archivo')
        else:
            print('ERROR en el metodo writeData')

    def strToBool(self, value):
        if value == 'True':
            return True
        else:
            return False
