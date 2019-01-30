#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona


import os

from src.config import RUTA_BASE
from src.model import DomesticAnimal, StreetAnimal


class Data(object):
    """Clase encargada de gestionar la recuperacion y escritura de datos en
     los registros de texto"""

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
        return os.path.join('data', dataName)

    def connectData(self, dataPath, mode):
        try:
            with open(dataPath, mode) as data:
                return data.readlines()
        except IOError as error:
            print('Error al Recuperar la informacion')
            print(error)
            return 'ERROR'

    def getData(self, param=None, value=None):
        """Metodo que obtiene los datos desde el archivo CSV y los almacena como objetos Animal de cada tipo"""
        dataFiltred = []
        if self.data != 'ERROR':
            rows = self.data
            # print(rows)

            if param != None and value != None:

                if param == 'id':
                    col = 0
                elif param == 'type':
                    col = 1
                elif param == 'domestic':
                    col = 2
                elif param == 'age':
                    col = 3
                elif param == 'gender':
                    col = 4
                elif param == 'attitude':
                    col = 5
                elif param == 'castrated':
                    col = 6

                for row in rows:
                    rowDat = row.split('\n')
                    rowDat = rowDat[0].split(',')
                    # print(rowDat)
                    # print(col)
                    if rowDat[col] == value:
                        if rowDat[2] == 'True':
                            animal = DomesticAnimal(int(rowDat[0]), rowDat[1], self.strToBool(rowDat[2]), int(
                                rowDat[3]), rowDat[4], rowDat[5],
                                self.strToBool(rowDat[6]), rowDat[7],
                                rowDat[8], self.strToBool(rowDat[9]))
                        else:
                            animal = StreetAnimal(int(rowDat[0]), rowDat[1],
                                                  self.strToBool(
                                                      rowDat[2]), int(rowDat[3]),
                                                  rowDat[4], rowDat[5], self.strToBool(
                                                      rowDat[6]),
                                                  rowDat[7], rowDat[8])
                        # print(animal)
                        dataFiltred.append(animal)
        else:
            print('Error al obtener la informacion')
        return dataFiltred

    def writeData(self, animalsList):
        """Metodo que escribe un objeto Animal en el archivo CSV"""
        try:
            with open(self.dataOutPath, 'w') as data:
                for animal in animalsList:
                    data.write('{}\n'.format(animal))
                print('Archivo escrito')
        except IOError as error:
            print('Algo salio mal')
            print(error)

    def strToBool(self, value):
        """Metodo que convierte un str a bool"""
        if value == 'True':
            return True
        else:
            return False
