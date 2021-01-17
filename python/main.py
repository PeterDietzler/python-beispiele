#!/user/bin/python3
import mod.sysinfo.systeminfo as get
import mod.gui.myGui as gui
import mod.suntimes.suntimes as sun
import mod.PlotGraph.plotGraph as pgraph
from os import system

print('-' * 40 + "Start" +'-' * 40)


get.systeminfo()
get.boottime()
get.cpuinfo()
get.raminfo()
get.gpuinfo()
get.netinfo()
               
print('-' * 40 + "Suntimes.py" +'-' * 40)
lat = 50.594
lng = 8.9673
tz  = 1  # +1 Stunder
print( "sunrice    : ", sun.rice    ( lat, lng, tz ))
print( "sunnoon    : ", sun.noon    ( lat, lng, tz ))
print( "sunset     : ", sun.set     ( lat, lng, tz ))
print( "sunDaytime : ", sun.daytime ( lat, lng, tz ))

print('-' * 40 + "myGUI.py" +'-' * 40)
gui.openGUI()

print("openStuff2()")
gui.openStuff2()

print('-' * 40 + "plptGraph.py" +'-' * 40)
pgraph.plptGraph()

print('-' * 40 + "webserver.py" +'-' * 40)

#system("firefox 'http://localhost:5000/' 'http://localhost:5000/templates?name=cat'")

system("firefox http://localhost:5000/ http://localhost:5000/templates?name=cat  &")
system( "python3 ../FlaskWebServer/startApp.py" )


print( "done" )


