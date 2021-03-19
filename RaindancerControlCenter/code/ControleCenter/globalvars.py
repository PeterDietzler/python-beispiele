import os
import platform

cwd = os.getcwd()



uname = platform.uname()

print(f"System: {uname.system}")

if uname.system == "Linux":
    myComPort = '/dev/ttyUSB1'
    myFrameWidth = 800
    myFrameHeight = 430

if uname.system == "Windows":
    myComPort = 'COM1'
    myFrameWidth = 800
    myFrameHeight = 430

myBaudRate = 115200
