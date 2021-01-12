import tkinter as tk
from plot import TPlot
from controller import myController
from globalvars import cwd
from globalvars import myFrameHeight
from globalvars import myFrameWidth
from globalvars import cwd
import time

from kst_start_class import TKstStart
import os

class PerPage(tk.Frame):

    def ButtonBackToMain_click(self, appClass):
        appClass.show_start_page()



    def __init__(self, parent, appClass):
        tk.Frame.__init__(self, parent, height=myFrameHeight, width=myFrameWidth)
        backgroundColor = '#362F2F'
        self.isActive = False
        self.myPlotL = TPlot(self, "not used", 500, 3, 1)
        self.myPlotR = TPlot(self, "not used", 500, 3, 1)

        self.myPlotL.pack(side="top", fill="both", expand=True)
        self.myPlotR.pack(side="top", fill="both", expand=True)

        #self.myPlotL.grid(row=0, column=0)
        #self.myPlotR.grid(row=1, column=0)
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_columnconfigure(0, weight=1)

        self.status_frame = tk.Frame(self, background=backgroundColor, width=myFrameWidth )
        self.status_frame.pack(side="bottom", fill="both", expand=False)

        #MainStatusLine=tk.StringVar()
        #MainStatusLine = "XXS"
        #Maintext = tk.Label(self.status_frame, text='no status',  textvariable=MainStatusLine, font=("Arial", 18), bg=backgroundColor, fg='white',  width=49, height=1,  anchor=tk.SW, justify=tk.LEFT )
        #Maintext.pack(side=tk.LEFT)

        ButtonBack1 = tk.Button(self.status_frame, text="Back To Main", command=lambda: self.ButtonBackToMain_click(appClass), justify=tk.LEFT)
        ButtonBack1.pack(side=tk.RIGHT)
        #ButtonBack1.place(x=myFrameWidth - 100, y=myFrameHeight - 20, height=20, width=100)

        self.a = 0
        self.b = 0
        self.c = 0

        self.kstStart = TKstStart()

    def Activate(self):
        self.isActive = True
        try:
            os.remove(cwd +"/log/PlotPer.txt")
        except OSError:
            pass

        f = open(cwd + "/log/PlotPer.txt", 'w+')
        #f.write("$per, ML, 0, 0, 0, MR, 0, 0, 0\r\n")
        f.close()

        self.kstStart.start(cwd + "/kst/testper.kst")

    def Deactivate(self):
        self.isActive = False
        self.myPlotL.deleteBuffer()
        self.myPlotR.deleteBuffer()
        self.kstStart.stop()  # close the kst prog

    def OnReceiveSerialData(self, dataObj):
        pass

        #if self.isActive:
        #    if dataObj.recievedList[0] == '$per':
        #        try:
        #            f = open( cwd + "/log/PlotPer.txt", 'a+')
        #            f.write("{}\n".format(dataObj.receivedMessage))
        #            f.close()
        #        except Exception as e:
        #            print('per: ', e)

        #if self.isActive:
        #    if dataObj.recievedList[0] == '$per':
        #        try:
        #            self.myPlotL.addPlotData(dataObj.recievedList[2],dataObj.recievedList[3],dataObj.recievedList[4])
        #            self.myPlotR.addPlotData(dataObj.recievedList[6],dataObj.recievedList[7],dataObj.recievedList[8])
        #        except Exception as e:
        #            print('per: ', e)


            # self.myPlotR.addPlotData(-self.a,-self.b,self.c)
            #self.a = self.a+0.5
            #if self.a>100:
            #    self.a=0
            #self.b = self.b + 0.6
            #if self.b>120:
            #    self.b=0
            #self.c = self.c + 0.7
            #if self.c>130:
            #    self.c=0
            #self.myPlotL.addPlotData(-self.a,self.b,self.c)
            #self.myPlotR.addPlotData(-self.a,-self.b,self.c)
            #self.myPlotL.addPlotData(-2, -2, -2)
            #self.myPlotR.addPlotData(2, 2, 2)
            #print("dlgkjfdsöglkfdsgöldfgödfjg")
