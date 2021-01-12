import tkinter as tk
from controller import myController
from globalvars import cwd
from globalvars import myFrameHeight
from globalvars import myFrameWidth



class ManualPage(tk.Frame):
    speedL=0
    speedR=0
    
    ActualState='stop'
        
    def ButtonForward_click(self, appClass):
        ManualPage.speedL=self.manualSpeedSlider.get()
        ManualPage.speedR=self.manualSpeedSlider.get()
        myController.sendData('pc.cm,500,500,'+str(ManualPage.speedL)+','+str(ManualPage.speedR)+'')


    def ButtonRight_click(self, appClass):
        ManualPage.speedR=20
        #to brake the inner wheel faster only 5 CM to drive
        myController.sendData('pc.cm,500,5,'+str(ManualPage.speedL)+','+str(ManualPage.speedR)+'')



    def ButtonLeft_click(self, appClass):
        ManualPage.speedL=20
        myController.sendData('pc.cm,5,500,'+str(ManualPage.speedL)+','+str(ManualPage.speedR)+'')

        
    def ButtonReverse_click(self, appClass):
        myController.sendData('pc.cm,-500,-500,-'+str(ManualPage.speedL)+',-'+str(ManualPage.speedR)+'')


    def ButtonStop_click(self, appClass):
        myController.sendData('pc.s')
        

    def buttonBlade_start_click(self, appClass):
        myController.sendData('z')

    def buttonBlade_stop_click(self, appClass):
        
        myController.sendData('t')

    def button_stop_all_click(self, appClass):
        myController.sendManualMode()

    def ButtonBackToMain_click(self, appClass):
        appClass.show_start_page()

    def __init__(self, parent, appClass):
        tk.Frame.__init__(self, parent, height=myFrameHeight, width=myFrameWidth)

        Frame1 = tk.Frame(self)
        Frame1.place(x=0, y=0, height=300, width=300)

        self.imgBladeStop = tk.PhotoImage(file=cwd + "/icons/bladeoff.png")
        self.imgBladeStart = tk.PhotoImage(file=cwd + "/icons/bladeon.png")
        self.imgForward = tk.PhotoImage(file=cwd + "/icons/forward.png")
        self.imgReverse = tk.PhotoImage(file=cwd + "/icons/reverse.png")
        self.imgLeft = tk.PhotoImage(file=cwd + "/icons/left.png")
        self.imgRight = tk.PhotoImage(file=cwd + "/icons/right.png")
        self.imgStop = tk.PhotoImage(file=cwd + "/icons/stop.png")
        self.imgStopAll = tk.PhotoImage(file=cwd + "/icons/stop all.png")

        self.ButtonForward = tk.Button(Frame1, image=self.imgForward, command=lambda: self.ButtonForward_click(appClass))
        self.ButtonForward.place(x=100, y=0, height=100, width=100)

        self.ButtonStop = tk.Button(Frame1, image=self.imgStop, command=lambda: self.ButtonStop_click(appClass))
        self.ButtonStop.place(x=100, y=100, height=100, width=100)

        self.ButtonRight = tk.Button(Frame1, image=self.imgRight, command=lambda: self.ButtonRight_click(appClass))
        self.ButtonRight.place(x=200, y=100, height=100, width=100)

        self.ButtonLeft = tk.Button(Frame1, image=self.imgLeft, command=lambda: self.ButtonLeft_click(appClass))
        self.ButtonLeft.place(x=0, y=100, height=100, width=100)

        self.ButtonReverse = tk.Button(Frame1, image=self.imgReverse, command=lambda: self.ButtonReverse_click(appClass))
        self.ButtonReverse.place(x=100, y=200, height=100, width=100)

        self.ButtonBladeStart = tk.Button(self, image=self.imgBladeStart, command=lambda: self.buttonBlade_start_click(appClass))
        self.ButtonBladeStart.place(x=400, y=80, width=100, height=50)
        self.ButtonBladeStop = tk.Button(self, image=self.imgBladeStop, command=lambda: self.buttonBlade_stop_click(appClass))
        self.ButtonBladeStop.place(x=400, y=130, width=100, height=80)

        self.ButtonStopAllManual = tk.Button(self, image=self.imgStopAll, command=lambda: self.button_stop_all_click(appClass))
        self.ButtonStopAllManual.place(x=400, y=250, width=100, height=130)

        self.manualSpeedSlider = tk.Scale(self, orient='horizontal', from_=20, to=100)
        self.manualSpeedSlider.place(x=0, y=300, width=300, height=80)
        tk.Label(self, text='SPEED', fg='green').place(x=0, y=300)

        self.ButtonBack1 = tk.Button(self, text="Back To Main", command=lambda: self.ButtonBackToMain_click(appClass))
        self.ButtonBack1.place(x=myFrameWidth - 100, y=myFrameHeight - 20, height=20, width=100)


    def OnReceiveSerialData(self,dataObj):
        #print('ManualPage' + dataObj.receivedMessage)
        pass
