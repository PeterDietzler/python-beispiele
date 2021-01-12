#
# Serial COM Port receive message event handler
# 8/17/2017, Dale Gambill
# When a line of text arrives from the COM port terminated by a \n character, this module will pass the message to
# the function specified by the instantiator of this class.
#
import serial
import sys
import time


class SerialPort:
    def __init__(self):
        self.comportName = ""
        self.baud = 0
        self.timeout = None
        self.ReceiveCallback = None
        self.isopen = False
        self.serialport = serial.Serial()
        self.buf = bytearray()

    def __del__(self):
        try:
            if self.serialport.is_open():
                self.serialport.close()
                print('SerialPort Destructor closing COM port')
        except:
            pass  # errors on shutdown

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.serialport.in_waiting))
            data = self.serialport.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)


    def RegisterReceiveCallback(self,aReceiveCallback):
        self.ReceiveCallback = aReceiveCallback

    def readSerial(self):
        if self.serialport.in_waiting != 0:
            line = self.readline()
            try:
                 line = line.decode('utf-8', errors='replace').strip("\r\n")
            except Exception as e:
                 print("Error in readSerial")
                 print(e)
                 line = ""

            if line != "" and self.ReceiveCallback is not None:
                self.ReceiveCallback(line)


    def IsOpen(self):
        return self.isopen

    def Open(self,portname,baudrate):
        if not self.isopen:
            # serialPort = 'portname', baudrate, bytesize = 8, parity = 'N', stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
            self.serialport.port = portname
            self.serialport.baudrate = baudrate
            self.serialport.bytesize = serial.EIGHTBITS
            self.serialport.parity = serial.PARITY_NONE
            self.serialport.stopbits = serial.STOPBITS_ONE
            self.serialport.xonxoff = 0
            self.serialport.rtscts = 0
            self.serialport.timeout = 0.0
            self.serialport.write_timeout = 0.0
            #self.serialport.BYTESIZES = serial.SEVENBITS

            try:
                self.serialport.open()
                self.isopen = True
                time.sleep(0.2)
                #self.serialport.flushInput()
                #self.serialport.flushOutput()  # clear the output buffer
            except:
                print("Error opening COM port: ", sys.exc_info()[0])


    def Close(self):
        if self.isopen:
            print("closing serial port")
            try:
                self.serialport.close()
                self.isopen = False
            except:
                print("Close error closing COM port: ", sys.exc_info()[0])

    def Send(self, message):
        if self.isopen:
            try:
                self.serialport.flushOutput()  # clear the output buffer
                # Ensure that the end of the message has both \r and \n, not just one or the other
                newmessage = message.strip()
                newmessage += '\r\n'
                self.serialport.write(newmessage.encode('utf-8'))
                #self.serialport.write(bytes(newmessage, 'utf-8'))
            except:
                print("Error sending message: ", sys.exc_info()[0] )
            else:
                return True
        else:
            return False







