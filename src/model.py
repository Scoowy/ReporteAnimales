#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona

import abc


class Animal(metaclass=abc.ABCMeta):
    """Clase abstracta que define un animal
    Domestico: PERRO,1,24,M,DOCIL,1,ETTO,JUAN GAHONA,UNION LOJANA,1
    Callejero: GATO,0,48,F,AGRESIVO,1,ANABELL M.,LA COLINA"""

    def __init__(self, id: int, type: str, domestic: bool, age: int, gender: str, attitude: str, castrated: bool):
        self.id = id
        self.type = type
        self.domestic = domestic
        self.age = age
        self.gender = gender
        self.attitude = attitude
        self.castrated = castrated

    @abc.abstractmethod
    def __str__(self):
        pass


class DomesticAnimal(Animal):
    """Clase que contiene la informacion de un animal domestico
    Domestico: PERRO,1,24,M,DOCIL,1,ETTO,JUAN GAHONA,UNION LOJANA,1"""

    def __init__(self, id: int, type: str, domestic: bool, age: int, gender: str, attitude: str, castrated: bool, residentialArea: str, ownerName: str, vaccinations: bool):
        super().__init__(id, type, domestic, age, gender, attitude, castrated)
        self.residentialArea = residentialArea
        self.ownerName = ownerName
        self.vaccinations = vaccinations

    def __str__(self):
        return '{},{},{},{},{},{},{},{},{},{}'.format(self.id, self.type, self.domestic, self.age, self.gender, self.attitude, self.castrated, self.residentialArea, self.ownerName, self.vaccinations)


class StreetAnimal(Animal):
    """Clase que contiene la informacion de un animal callejero
    Callejero: GATO,0,48,F,AGRESIVO,1,ANABELL M.,LA COLINA"""

    def __init__(self, id: int, type: str, domestic: bool, age: int, gender: str, attitude: str, castrated: bool, foundArea: str, findingName: str):
        super().__init__(id, type, domestic, age, gender, attitude, castrated)
        self.foundArea = foundArea
        self.findingName = findingName

    def __str__(self):
        return '{},{},{},{},{},{},{},{},{}'.format(self.id, self.type, self.domestic, self.age, self.gender, self.attitude, self.castrated, self.foundArea, self.findingName)


class AnimalsList(metaclass=abc.ABCMeta):
    """Clase abstracta que define las listas de animales"""

    def __init__(self, nameList: str, animals=[]):
        self.animals = animals
        self.nameList = nameList
        self.lastId = self.maxId()

    @abc.abstractmethod
    def addAnimal(self):
        pass

    def maxId(self):
        ids = []
        for animal in self.animals:
            ids.append(animal.id)
        if len(ids) == 0:
            return 0
        else:
            return max(ids)

    @abc.abstractmethod
    def __str__(self):
        pass


class DomesticAnimalList(AnimalsList):
    """Clase que contiene una lista de animales domesticos"""

    def __init__(self, nameList, animals=[]):
        super().__init__(nameList, animals=animals)

    def addAnimal(self, id: int, type: str, domestic: bool, age: int, gender: str, attitude: str, castrated: bool, residentialArea: str, ownerName: str, vaccinations: bool):
        """Metodo que añade un nuevo animal Domestico"""
        animal = DomesticAnimal(id, type, domestic, age, gender, attitude,
                                castrated, residentialArea, ownerName, vaccinations)
        self.animals.append(animal)
        self.maxId()

    def __str__(self):
        return ''


class StreetAnimalList(AnimalsList):
    """Clase que contiene una lista de animales salvajes"""

    def __init__(self, nameList, animals=[]):
        super().__init__(nameList, animals=animals)

    def addAnimal(self, id: int, type: str, domestic: bool, age: int, gender: str, attitude: str, castrated: bool, foundArea: str, findingName: str):
        """Metodo que añade un nuevo animal Callejero"""
        animal = StreetAnimal(id, type, domestic, age, gender, attitude,
                              castrated, foundArea, findingName)
        self.animals.append(animal)
        self.maxId()

    def __str__(self):
        return ''
