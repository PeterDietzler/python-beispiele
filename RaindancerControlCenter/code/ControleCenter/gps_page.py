import tkinter as tk
from controller import myController
from globalvars import cwd
from globalvars import myFrameHeight
from globalvars import myFrameWidth



class GPSPage(tk.Frame):


    def ButtonBackToMain_click(self, appClass):
        print("GO TO STARTPAGE")
        appClass.show_start_page()


    def BtnGpsRecordStart_click(self, appClass):
        #mygpsRecord.start()
        pass

    def BtnGpsRecordStop_click(self, appClass):
        #mygpsRecord.stop()
        pass

    def __init__(self, parent, appClass):

        tk.Frame.__init__(self, parent, height=myFrameHeight, width=myFrameWidth)

        FrameGps = tk.Frame(self, borderwidth="1", relief=tk.SOLID)
        FrameGps.place(x=20, y=40, width=600, height=300)
        tk.Label(self, text='The gps run as service and write into directory /gpsdata/').place(x=10, y=15)
        BtnGpsRecordStart = tk.Button(FrameGps, command=lambda: self.BtnGpsRecordStart_click(appClass), text="Start")
        BtnGpsRecordStart.place(x=80, y=50, height=25, width=60)
        BtnGpsRecordStop = tk.Button(FrameGps, command=lambda: self.BtnGpsRecordStop_click(appClass), text="Stop")
        BtnGpsRecordStop.place(x=10, y=50, height=25, width=60)

        ButtonBack1 = tk.Button(self, text="Back To Main", command=lambda: self.ButtonBackToMain_click(appClass))
        ButtonBack1.place(x=myFrameWidth - 100, y=myFrameHeight - 40, height=40, width=100)

    def OnReceiveSerialData(self, dataObj):
        pass
