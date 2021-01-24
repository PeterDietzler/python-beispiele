#!/usr/bin/python3

# This Python file uses the following encoding: utf-8

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets, uic


import PyQt5.QtWidgets as widget

sys.path.append(".")

import MainWindow




if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	GUI = MainWindow.myMainWindow(app)
	
	


