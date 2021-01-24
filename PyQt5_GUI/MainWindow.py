#!/usr/bin/python

# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets, uic
import time
from PyQt5.QtGui import QPixmap, QImage 
import videoCapture 

print('Import MainWindow')


class myMainWindow:
	def __init__(self, applikation):
		super().__init__()
		print('myMainWindow Loaded')
		self.applikation = applikation
		self.w = uic.loadUi("MainWindow.ui")
		self.w.pushButtonEnde.clicked.connect(  self.clickButtonEnde)
		self.w.pushButtonStart.clicked.connect( self.clickButtonStart)
		# self.w.tabWidget.ResultTab.pushButtonOpenCam.clicked.connect( self.clickButtonOpenCam)
		self.w.pushButtonOpenCam.clicked.connect( self.clickButtonOpenCam)

		self.w.show()
		self.applikation.exec_()

	def clickButtonEnde(self):
		print("clickButtonEnde")
		self.doClose()
		
		
	def load(self):
		print('load')

	def getVal(self):
		return self.val

	def printname(self):
			print('hallo')
	
	def clickButtonOpenCam(self):
		print("clickButtonOpenCam")
		self.vc = videoCapture.videoCapture(0)
		self.vc.openCam()
		self.vc.showFrame()

	def clickButtonStart(self):
		print("clickButtonStart")
		
	def doClose(self):
		self.applikation.exit()
 



"""
		while True:
			cvRGBImg = self.vc.getFrame()
			qimg   = QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QImage.Format_RGB888)
			pixmap = QPixmap.fromImage(qimg)
			item = QWidgets.QGraphicsPixmapItem(pixmap)
			scene = QWidgets.QGraphicsScence(self)
			scene.addItem(item)
			self.w.graphicsView.setScene(scene)
"""
