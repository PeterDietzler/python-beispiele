#!/bin/python3
import mod.sysinfo.systeminfo as get


import mod.gui.myGui as gui


get.systeminfo()
get.boottime()
get.cpuinfo()
get.raminfo()
get.gpuinfo()
get.netinfo()

gui.openGUI()
gui.openStuff2()
