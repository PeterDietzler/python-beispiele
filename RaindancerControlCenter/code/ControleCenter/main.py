import tkinter as tk
from tkinter import font as tkfont
from controller import myController
from globalvars import cwd
from start_page import StartPage
from auto_page import AutoPage
from manual_page import ManualPage
from console_page import ConsolPage
from gps_page import GPSPage
from camera_page import CameraPage
from per_page import PerPage
from tkinter import messagebox

# globals
#logFile = none
print("Work directory: " + cwd)




class MyApp(tk.Tk):

    def on_closing(self):
        myController.closeSerial()
        self.destroy()
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #    print("HELLO")

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("ARDUMOWER - Raindancer Controlle Center")

        #self.attributes('-fullscreen', True)
        #self.bind('<Escape>', lambda e: self.destroy())

        #self.overrideredirect(True)
        #self.wm_state('zoomed')

        #self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        #self.focus_set()  # <-- move focus to this widget
        #self.bind("<Escape>", lambda e: e.widget.quit())

        #w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        #self.geometry("%dx%d+0+0" % (w, h))
        #self.resizable(width=False, height=False)
        #self.geometry("800x430")
        #screenWidth = self.winfo_screenwidth()
        #screenHeight = self.winfo_screenheight()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.currentFrame = None
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, AutoPage, ManualPage, ConsolPage, GPSPage, CameraPage, PerPage):
            page_name = F.__name__
            frame = F(parent=container, appClass=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.currentFrame = self.frames[page_name]
        self.currentFrame.tkraise()

    def deactivateFrames(self):
        self.frames["PerPage"].Deactivate()

    def show_start_page(self):
        self.deactivateFrames()
        self.show_frame("StartPage")

    def show_auto_page(self):
        self.deactivateFrames()
        self.show_frame("AutoPage")

    def show_manual_page(self):
        self.deactivateFrames()
        self.show_frame("ManualPage")

    def show_consol_page(self):
        self.deactivateFrames()
        self.show_frame("ConsolPage")

    def show_gps_page(self):
        self.deactivateFrames()
        self.show_frame("GPSPage")

    def show_camera_page(self):
        self.deactivateFrames()
        self.show_frame("CameraPage")

    def show_per_page(self):
        self.deactivateFrames()
        self.show_frame("PerPage")
        self.currentFrame.Activate()

    def OnReceiveSerialData(self, dataObj):
        frame = self.frames["StartPage"]
        frame.OnReceiveSerialData(dataObj)
        frame = self.frames["AutoPage"]
        frame.OnReceiveSerialData(dataObj)
        frame = self.frames["ManualPage"]
        frame.OnReceiveSerialData(dataObj)
        frame = self.frames["ConsolPage"]
        frame.OnReceiveSerialData(dataObj)
        frame = self.frames["GPSPage"]
        frame.OnReceiveSerialData(dataObj)
        frame = self.frames["CameraPage"]
        frame.OnReceiveSerialData(dataObj)
        frame = self.frames["PerPage"]
        frame.OnReceiveSerialData(dataObj)

def MainLoop():
    myController.readSerial()
    '''//app.after(10, MainLoop)  # check serial again soon'''
    app.after(10, MainLoop)  # check serial again soon


if __name__ == "__main__":
    app = MyApp()
    myController.RegisterDataReceiveCallback(app.OnReceiveSerialData)
    app.after(100, MainLoop)
    app.mainloop()
