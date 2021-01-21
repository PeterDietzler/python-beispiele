# This Python file uses the following encoding: utf-8

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize

from PyQt5 import QtWidgets, uic
sys.path.append(".")



#import MainWindow

class MainWindow:
    def __init__(self,val):
        #QtWidgets.QMainWindow.__init__(self)
        self.val=val

    def getVal(self):
        return self.val

    def load(self):
        MainWindow = uic.loadUi("MainWindow.ui")
        MainWindow.show()

    def printname(self):
        print('hallo')

def startWindow():
    MainWindow = uic.loadUi("MainWindow.ui")
    MainWindow.show()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow.load
    w = MainWindow(5)
    Val = w.getVal()
    print(Val)
    #w.load()
    #startWindow
    MainWindow = uic.loadUi("MainWindow.ui")
    MainWindow.show()

    sys.exit( app.exec_() )



