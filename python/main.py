#!/bin/python3
import mod.sysinfo.systeminfo as get
import mod.gui.myGui as gui
import mod.sun.suntimes as sunget


get.systeminfo()
get.boottime()
get.cpuinfo()
get.raminfo()
get.gpuinfo()
get.netinfo()
               
sunget.sunsetxy( 50.594855214374064, 8.967300469313207 )

print('-' * 40 + "myGUI.py" +'-' * 40)

gui.openGUI()
gui.openStuff2()


