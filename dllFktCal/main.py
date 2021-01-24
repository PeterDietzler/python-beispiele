from os import system
from ctypes import *


system("gcc -shared -o testdll.so -fPIC testdll.c")


p = cdll.LoadLibrary("./testdll.so")

p.connect()


def HalloWelt():
	return p.HalloWelt() 
	
def randNum():
	return p.randNum()

def  addNum( a, b):
	return p.addNum(a,b)

def  getText( text):
	return p.getText(text)

def printText( text):
	p.printText( text)

	
	
print("HalloWelt() return:" , HalloWelt()   )
print("randNum() return  :" , randNum()     )
print("addNum() return   :" , addNum( 5, 5) )
print("printText() return   :") 
printText("Text print:")
text = "hallo kleiner Sch...er"
print("getText('" + text + "') return :" + str( getText(text)) )



