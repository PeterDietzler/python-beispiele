import tkinter as tk
from controller import myController
from globalvars import cwd
from globalvars import myFrameHeight
from globalvars import myFrameWidth



class CameraPage(tk.Frame):

    def BtnStreamVideoStart_click(self, appClass):
        if CamVar1.get() == 1:
            myStreamVideo.start(0)
            webbrowser.open("http://localhost:8000/index.html") #war azgeklammert

        else:
            myStreamVideo.start(0)
        pass

    def BtnStreamVideoStop_click(self, appClass):
        # myStreamVideo.stop()
        pass

    def ButtonBackToMain_click(self, appClass):
        appClass.show_start_page()


    def BtnGpsRecordStart_click(self, appClass):
        #mygpsRecord.start()
        pass

    def BtnGpsRecordStop_click(self, appClass):
        #mygpsRecord.stop()
        pass

    def __init__(self, parent, appClass):

        tk.Frame.__init__(self, parent, height=myFrameHeight, width=myFrameWidth)

        CamVar1 = tk.IntVar()

        FrameStreamVideo = tk.Frame(self, borderwidth="1", relief=tk.SOLID)
        FrameStreamVideo.place(x=20, y=30, width=600, height=300)
        OptBtnStreamVideo1 = tk.Radiobutton(FrameStreamVideo, text="320*240", relief=tk.SOLID, variable=CamVar1,
                                            value=0, anchor='nw').place(x=10, y=10, width=250, height=20)
        OptBtnStreamVideo2 = tk.Radiobutton(FrameStreamVideo, text="640*480", relief=tk.SOLID, variable=CamVar1,
                                            value=1, anchor='nw').place(x=10, y=30, width=250, height=20)
        tk.Label(FrameStreamVideo,
                 text='To view the vidéo stream use a browser http://(Your PI IP Adress and):8000/index.html').place(x=10, y=180)
        BtnStreamVideoStart = tk.Button(FrameStreamVideo, command=lambda: self.BtnStreamVideoStart_click(appClass), text="Start")
        BtnStreamVideoStart.place(x=180, y=250, height=25, width=60)
        BtnStreamVideoStop = tk.Button(FrameStreamVideo, command=lambda: self.BtnStreamVideoStop_click(appClass), text="Stop")
        BtnStreamVideoStop.place(x=10, y=250, height=25, width=60)

        ButtonBack1 = tk.Button(self, text="Back To Main", command=lambda: self.ButtonBackToMain_click(appClass))
        ButtonBack1.place(x=myFrameWidth - 100, y=myFrameHeight - 40, height=40, width=100)

    def OnReceiveSerialData(self, dataObj):
        pass
