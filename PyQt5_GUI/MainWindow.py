#!/usr/bin/python

# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget


print('MainWindow Loaded')


class MainWindow():
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        pass

    def load(self):
        MainWindow = uic.loadUi("MainWindow.ui")
        MainWindow.show()



def printname():
    print('hallo')

