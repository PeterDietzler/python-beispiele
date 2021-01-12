import os

cwd = os.getcwd()


#ifdef WINDOWS
myComPort = 'COM1'
myFrameWidth = 800
myFrameHeight = 430
#endif

#ifdef PI
#PRE myComPort = '/dev/ttyACM0'
#PRE myFrameWidth = 800
#PRE myFrameHeight = 430
#endif

myBaudRate = 115200
