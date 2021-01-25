from os import system
from ctypes import *
import platform

uname = platform.uname()

print(f"System: {uname.system}")

if uname.system == "Linux":
    system("gcc -shared -o testdll.so -fPIC testdll.c")
    p = cdll.LoadLibrary("./testdll.so")

if uname.system == "Windows":
    system("g++ -shared -o testdll.dll -fPIC testdll.c")
    p = cdll.LoadLibrary("./testdll.dll")

p.connect()

def HalloWelt():
    return p.HalloWelt() 

def randNum():
    return p.randNum()

def addNum( a, b):
    return p.addNum(a,b)

def getText(text):
    return p.getText(text)

def printText( text):
    p.printText( text)
    
print("HalloWelt() return:" , HalloWelt()   )
print("randNum() return  :" , randNum()     )
print("addNum() return   :" , addNum( 5, 5) )
print("printText() return   :") 
printText("Text print:")
mytext = "hallo kleiner Sch...er"
print("getText('" + mytext + "') return :" + str( getText(mytext)) )



