import serial_rx_tx
import time
from globalvars import myComPort
from globalvars import myBaudRate
from tkinter import messagebox
#import logging
from globalvars import cwd

class Tdata:

    def __init__(self):
        self.serialPort = serial_rx_tx.SerialPort()
        self.serialPort.Open(myComPort, myBaudRate)
        self.serialPort.RegisterReceiveCallback(self.OnReceiveSerialData)
        self.ReceiveCallback = None
        self.receivedMessage = ""
        self.recievedList = []

        self.temp = 20
        self.humidity = 40
        self.batVoltage = 29
        #logging.basicConfig(filename=cwd + "/log/debug.log", level=logging.DEBUG)


    def RegisterReceiveCallback(self, aReceiveCallback):
        self.ReceiveCallback = aReceiveCallback

    def closeSerial(self):
        self.serialPort.Close()

    def readSerial(self):
        self.serialPort.readSerial()

    def sendData(self, message):

        if self.serialPort.IsOpen():
            message = message.rstrip(' \r\n')
            if len(message) > 0:
                message += '\r\n'
                print("SerialSend: " + message)
                self.serialPort.Send(message)
        else:
            messagebox.showinfo("Title", "Not sent - COM port is closed\r\n")

    def OnReceiveSerialData(self, message):
        self.receivedMessage = message
        #logging.info(self.receivedMessage)

        #print(self.receivedMessage)

        self.recievedList.clear()
        self.recievedList = message.split(",")

        if self.recievedList[0][:1] == '$':  # the first digit is $ so something to do

            # print out list for debugging
            # for item in self.recievedList:
            #    print(item)

            if self.recievedList[0] == '$temp':
                try:
                    self.temp = (round(float(self.recievedList[1]), 2))
                    f = open(cwd + "/log/PlotTemp.txt", 'a+')
                    f.write("{}\n".format(time.strftime("%X,") + self.receivedMessage))
                    f.close()
                except Exception as e:
                   print('$temp received: ', e)

            if self.recievedList[0] == '$batV':
                try:
                    self.batVoltage = (round(float(self.recievedList[1]), 2))
                    f = open(cwd + "/log/PlotBat.txt", 'a+')
                    f.write("{}\n".format(time.strftime("%X,") + self.receivedMessage))
                    f.close()
                except Exception as e:
                    print('$batV received: ', e)

            if self.recievedList[0] == '$per':
                try:
                    f = open(cwd + "/log/PlotPer.txt", 'a+')
                    f.write("{}\n".format(self.receivedMessage))
                    f.close()
                except Exception as e:
                    print('per: ', e)

        else:
            # print(self.receivedMessage)
            pass

        if self.ReceiveCallback is not None:
            self.ReceiveCallback(self)

