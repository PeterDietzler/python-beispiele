import tkinter as tk
from controller import myController
from globalvars import cwd
from globalvars import myFrameHeight
from globalvars import myFrameWidth
from tkinter import messagebox



class StartPage(tk.Frame):

    def ButtonAuto_click(self, appClass):
        appClass.show_auto_page();

    def ButtonManual_click(self, appClass):
        myController.sendManualMode()
        appClass.show_manual_page()

    def ButtonCamera_click(self, appClass):
        appClass.show_camera_page()

    def ButtonConsole_click(self, appClass):
        appClass.show_consol_page()

    def ButtonGps_click(self, appClass):
        appClass.show_gps_page()

    def ButtonPer_click(self, appClass):
        appClass.show_per_page()

    def ButtonPowerOff_click(self, appClass):
        returnval=messagebox.askyesno('Info',"Are you sure you want to shutdown all the PCB ?")
        if returnval:
            myController.sendData('poweroff')
        pass

    def ButtonBackToMain_click(self, appClass):
        # MainPage.tkraise()
        pass

    def __init__(self, parent, appClass):
        tk.Frame.__init__(self, parent, height=myFrameHeight, width=myFrameWidth)

        backgroundColor = '#362F2F'
        self.configure(background= backgroundColor)


        self.imgArdumower = tk.PhotoImage(file=cwd + "/icons/ardumower.png")
        self.imgManual = tk.PhotoImage(file=cwd + "/icons/manual1.png")
        self.imgAuto = tk.PhotoImage(file=cwd + "/icons/auto1.png")
        # self.imgTest=tk.PhotoImage(file=cwd + "/icons/test.png")
        self.imgConsole = tk.PhotoImage(file=cwd + "/icons/console1.png")
        # self.imgSetting=tk.PhotoImage(file=cwd + "/icons/setting.png")
        self.imgPowerOff = tk.PhotoImage(file=cwd + "/icons/off2.png")
        # self.imgPlot=tk.PhotoImage(file=cwd + "icons/plot.png")
        # self.imgSchedule=tk.PhotoImage(file=cwd + "/icons/schedule.png")
        self.imgCamera = tk.PhotoImage(file=cwd + "/icons/camera1.png")
        self.imgGps = tk.PhotoImage(file=cwd + "/icons/gps1.png")
        self.imgDummy = tk.PhotoImage(file=cwd + "/icons/dummy.png")
        self.imgPer = tk.PhotoImage(file=cwd + "/icons/plot.png")

        self.top_frame = tk.Frame(self, background=backgroundColor, height=133,width=myFrameWidth)
        self.mid_frame = tk.Frame(self, background=backgroundColor, height=133,width=myFrameWidth)
        self.bottom_frame = tk.Frame(self, background=backgroundColor, height=133,width=myFrameWidth)
        self.status_frame = tk.Frame(self, background=backgroundColor, width=myFrameWidth)
        self.top_frame.pack()
        self.mid_frame.pack()
        self.bottom_frame.pack()
        self.status_frame.pack(pady=3, anchor=tk.N)

        ButtonManual = tk.Button(self.top_frame,image=self.imgAuto, borderwidth=0, command = lambda: self.ButtonAuto_click(appClass), height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonManual.grid(row=0, column=0, padx=(6, 3), pady=(6, 3))
        ButtonManual = tk.Button(self.top_frame,image=self.imgManual, borderwidth=0,command = lambda: self.ButtonManual_click(appClass), height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonManual.grid(row=0, column=1, padx=3, pady=(6, 3))
        ButtonCamera = tk.Button(self.top_frame, image=self.imgCamera, borderwidth=0, command = lambda: self.ButtonCamera_click(appClass), height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonCamera.grid(row=0, column=2, padx=3, pady=(6,3))
        ButtonConsole = tk.Button(self.top_frame,image=self.imgConsole, borderwidth=0, command = lambda: self.ButtonConsole_click(appClass), height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonConsole.grid(row=0, column=3, padx=3, pady=(6,3))
        ButtonGps = tk.Button(self.top_frame, image=self.imgGps, borderwidth=0, command = lambda: self.ButtonGps_click(appClass), height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonGps.grid(row=0, column=4, padx=3, pady=(6,3))
        
        ButtonDummy = tk.Button(self.top_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)


        ButtonDummy.grid(row=0, column=5, padx=3, pady=(6,3))

        # Mid Frame
        ButtonPer = tk.Button(self.mid_frame, image=self.imgPer, borderwidth=0, command = lambda: self.ButtonPer_click(appClass), height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonPer.grid(row=0, column=0, padx=(6,3), pady=3)
        ButtonDummy = tk.Button(self.mid_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)

        ButtonDummy.grid(row=0, column=1, padx=3, pady=3)

        ButtonDummy = tk.Button(self.mid_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)

        ButtonDummy.grid(row=0, column=2, padx=3, pady=3)
        ButtonDummy = tk.Button(self.mid_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=3, padx=3, pady=3)
        ButtonDummy = tk.Button(self.mid_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=4, padx=3, pady=3)
        ButtonDummy = tk.Button(self.mid_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=5, padx=3, pady=3)

        # Bottom Frame
        ButtonDummy = tk.Button(self.bottom_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=0, padx=(6,3), pady=3)
        ButtonDummy = tk.Button(self.bottom_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=1, padx=3, pady=3)
        ButtonDummy = tk.Button(self.bottom_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=2, padx=3, pady=3)
        ButtonDummy = tk.Button(self.bottom_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=3, padx=3, pady=3)
        ButtonDummy = tk.Button(self.bottom_frame, image=self.imgDummy, borderwidth=0, height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonDummy.grid(row=0, column=4, padx=3, pady=3)
        ButtonPowerOff = tk.Button(self.bottom_frame, image=self.imgPowerOff, borderwidth=0, command = lambda: self.ButtonPowerOff_click(appClass), height=120, width=120, background=backgroundColor, highlightthickness=0, relief=tk.FLAT,activebackground=backgroundColor)
        ButtonPowerOff.grid(row=0, column=5, padx=3, pady=3 )

        # Statusbar
        MainStatusLine=tk.StringVar()
        MainStatusLine = "XXS"
        Maintext = tk.Label(self.status_frame, text='no status',  textvariable=MainStatusLine, font=("Arial", 18), bg=backgroundColor, fg='white',  width=56, height=1,  anchor=tk.SW, justify=tk.LEFT )
        Maintext.pack()




    def OnReceiveSerialData(self, dataObj):
        #print('StartPage' + dataObj.receivedMessage)
        pass
