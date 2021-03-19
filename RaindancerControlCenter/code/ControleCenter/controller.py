from data import  Tdata


class Tcontroller:

    def __init__(self):
        self. myData = Tdata()

    def __del__(self):
        pass

    def RegisterDataReceiveCallback(self, aReceiveCallback):
        self.myData.RegisterReceiveCallback(aReceiveCallback)

    def closeSerial(self):
        self.myData.closeSerial()

    def readSerial(self):
        self.myData.readSerial()

    def sendData(self, message):
        self.myData.sendData(message)

    def sendManualMode(self):
        self.sendData('M')

    def sendAutoMode(self):
        self.sendData('A')

    def sendTpt(self):
        self.sendData('tpt')

    def sendGohome(self):
        self.sendData('gohome')

    def sendReset(self):
        self.sendData('reset')

    def sendHelp(self):
        self.sendData('H')


myController = Tcontroller()
