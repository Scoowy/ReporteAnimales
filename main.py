#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scoowy - Juan Gahona

from tkinter import Tk
from tkinter.ttk import Style

from src import controller as ctr
from src import config as cfg

'''Reporte Animales: Sin definir '''

__author__ = 'Scoowy - Juan Gahona'
__title__ = cfg.TITLE_MAIN
__date__ = '03/12/2018'
__version__ = cfg.VERSION
__license__ = ''


def main():
    # Definir la ventana principal
    root = Tk()
    # Propiedades de la ventana principal
    # root.geometry('{}x{}'.format(cfg.WITDH_MAIN, cfg.HEIGH_MAIN))
    root.minsize(cfg.WITDH_MAIN, cfg.HEIGH_MAIN)
    root.title(cfg.TITLE_MAIN)

    # Configuracion de Estilos generales
    styles = Style()

    # Referencia del root al controlador
    controller = ctr.C_Main(root)

    # Ejecutamos ciclo principal del la ventana
    root.mainloop()


if __name__ == "__main__":
    main()
