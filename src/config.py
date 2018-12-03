#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona

import os

# Info general
VERSION = '0.0.1'
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

# Dimensiones de la ventana principal
WITDH_MAIN = 460
HEIGH_MAIN = 370
TITLE_MAIN = 'ReporteAnimaless - v{}'.format(VERSION)

# Configuracion del archivo data.txt
DATA_PATH = os.path.join(RUTA_BASE, 'data.txt')
DATA_SEPARATOR = ','
