import tkinter as tk
from controller import myController
from globalvars import cwd
from globalvars import myFrameHeight
from globalvars import myFrameWidth



class AutoPage(tk.Frame):

    def button_home_click(self, appClass):
        myController.sendGohome()

    def ButtonStartMow_click(self, appClass):
        myController.sendAutoMode()

    def button_track_click(self, appClass):
        myController.sendTpt()

    def button_stop_all_click(self, appClass):
        myController.sendManualMode()

    def ButtonBackToMain_click(self, appClass):
        appClass.show_start_page()


    def __init__(self, parent, appClass):
        tk.Frame.__init__(self, parent, height=myFrameHeight, width=myFrameWidth)

        self.imgHome=tk.PhotoImage(file=cwd + "/icons/home.png")
        self.imgTrack=tk.PhotoImage(file=cwd + "/icons/track.png")
        self.imgStopAll=tk.PhotoImage(file=cwd + "/icons/stop all.png")
        self.imgstartMow=tk.PhotoImage(file=cwd + "/icons/startmow.png")

        self.Frame2= tk.Frame(self)
        self.Frame2.place(x=10, y=180, height=60, width=100)
        self.Frame2.configure(borderwidth="3",relief=tk.GROOVE,background="#d9d9d9",highlightbackground="#d9d9d9",highlightcolor="black")

        self.batFrame = tk.Label(self.Frame2,text="BATTERY",fg='green')
        self.batFrame.pack(side='top',anchor='n')
        self.batLabel = tk.Label(self.Frame2, text = '0', fg='red',font=("Arial", 20))
        self.batLabel.pack(side='bottom',anchor='n')

        self.Frame3= tk.Frame(self)
        self.Frame3.place(x=130, y=180, height=60, width=100)
        self.Frame3.configure(borderwidth="3",relief=tk.GROOVE,background="#d9d9d9",highlightbackground="#d9d9d9",highlightcolor="black")

        self.tempFrame = tk.Label(self.Frame3,text="TEMPERATURE",fg='green')
        self.tempFrame.pack(side='top',anchor='n')
        self.tempLabel = tk.Label(self.Frame3, fg='red',text = "0", font=("Arial", 20))
        self.tempLabel.pack(side='bottom',anchor='n')

        self.Frame1 = tk.Frame(self)
        self.Frame1.place(x=10, y=20, height=150, width=130)
        self.batText = tk.Label(self.Frame1,text="Battery",fg='green')
        self.batText.pack(side='top',anchor='w')

        #RdBtn_Random=tk.Radiobutton(Frame1, text="Random", variable=tk_mowingPattern, value=0).pack(side='top',anchor='w')
        #RdBtn_ByLane=tk.Radiobutton(Frame1, text="By Lane", variable=tk_mowingPattern, value=1).pack(side='top',anchor='w')
        #RdBtn_Perimeter=tk.Radiobutton(Frame1, text="Perimeter", variable=tk_mowingPattern, value=2).pack(side='top',anchor='w')
        self.ButtonStartMow = tk.Button(self, image=self.imgstartMow, command =  lambda: self.ButtonStartMow_click(appClass))
        self.ButtonStartMow.place(x=130,y=0,width=100, height=130)
        self.Buttonhome = tk.Button(self, image=self.imgHome, command =  lambda: self.button_home_click(appClass))
        self.Buttonhome.place(x=250,y=0,width=100, height=130)
        self.Buttontrack = tk.Button(self, image=self.imgTrack, command =  lambda: self.button_track_click(appClass))
        self.Buttontrack.place(x=380,y=0,width=100, height=130)
        self.ButtonStopAllAuto = tk.Button(self, image=self.imgStopAll, command = lambda: self.button_stop_all_click(appClass))
        self.ButtonStopAllAuto.place(x=500,y=0,width=100, height=130)

        self.ButtonBack1 = tk.Button(self, text="Back To Main", command = lambda: self.ButtonBackToMain_click(appClass))
        self.ButtonBack1.place(x=myFrameWidth -100, y=myFrameHeight - 40, height=40, width=100)

    def OnReceiveSerialData(self, dataObj):
        self.tempLabel['text'] = dataObj.temp
        self.batLabel['text'] = dataObj.batVoltage
