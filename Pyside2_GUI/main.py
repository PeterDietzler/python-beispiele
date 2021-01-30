#!/usr/bin/python3

# This Python file uses the following encoding: utf-8

# Import PySide2 classes
import sys
from PySide2 import QtCore, QtWidgets

# Create a Qt application
app = QtWidgets.QApplication(sys.argv)

# Create a Window
mywindow = QtWidgets.QWidget()
mywindow.resize(1000, 700)
mywindow.setWindowTitle('Hello, World! WindowTitle')

# Create a label and display it all together
mylabel0 = QtWidgets.QLabel(mywindow)
mylabel0.setText('Hello, World! 100,100,100,100')
mylabel0.setGeometry(QtCore.QRect(100, 100, 100, 100))

# Create a label and display it all together
mylabel = QtWidgets.QLabel(mywindow)
mylabel.setText('Hello, World! 200,200,200,200')
mylabel.setGeometry(QtCore.QRect(200, 200, 200, 200))

mywindow.show()

# Enter Qt application main loop
sys.exit(app.exec_())