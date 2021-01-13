import time
import tkinter as tk
from controller import myController
from globalvars import cwd
from globalvars import myFrameHeight
from globalvars import myFrameWidth
from metroDesign import Metro_Button

class ConsolPage(tk.Frame):

    def ButtonSaveReceived_click(self, appClass):
        fileName = cwd + "/log/" + time.strftime("%Y%m%d%H%M") + "_Received.txt"
        with open(fileName, "w") as f:
            f.write(self.txtRecu.get('1.0', 'end'))
        fileName = cwd + "/log/" + time.strftime("%Y%m%d%H%M") + "_Send.txt"
        with open(fileName, "w") as f:
            f.write(self.txtSend.get('1.0', 'end'))
        fileName = cwd + "/log/" + time.strftime("%Y%m%d%H%M") + "_Console.txt"
        with open(fileName, "w") as f:
            f.write(self.txtConsoleRecu.get('1.0', 'end'))
        self.txtConsoleRecu.insert(tk.END, 'All console files are saved\n')

    def ButtonBackToMain_click(self, appClass):
        appClass.show_start_page()

    def ButtonChangeAutoScroll_click(self, appClass):
        self.stopAutoScroll = not self.stopAutoScroll;

        if self.stopAutoScroll:
            self.ButtonToggleScroll.configure(text="Run")
        else:
            self.ButtonToggleScroll.configure(text="Stop")

    def SendDBClick(self, event):
        # Accept only one double click per second
        # This is for bouncing of the double click sometimes
        ts = time.time()
        if ts-self.timeCalledDB < 0.5:
            return
        self.timeCalledDB = ts

        current_line = self.txtSend.index(tk.CURRENT)
        current_line = current_line.split(".")
        current_line = current_line[0]
        line_break = 0
        line_text = ""

        char = self.txtSend.get("%s.%d" % (current_line, line_break))
        while char != "\n":
            line_text += char
            line_break += 1
            char = self.txtSend.get("%s.%d" % (current_line, line_break))

        line_text = line_text.strip()
        if line_text == "Auto":
            line_text = "A"
        elif line_text == "Manual":
            line_text = "M"
        elif line_text == "Help":
            line_text = "H"
        elif line_text == "Reset":
            line_text = "reset"
        elif line_text == "Error":
            line_text = "error"
        elif line_text == "History":
            line_text = "show.hist"
        else:
            line_text = line_text
        if line_text != "":
            myController.sendData(line_text)
            self.txtConsoleRecu.insert('1.0', time.strftime("%X ") + 'Send out: ' + line_text + '\n')
            self.txtRecu.insert('1.0', time.strftime("%X ") + 'Send out: ' + line_text + '\n')



    def configureEvent(self,event):
        pass
        #w, h = event.width, event.height
        #self.panedwindow.paneconfigure(self.bottom_frame, height=200)
        #self.panedwindow.update()
        #self.top_frame(height=h*0.7)
        #self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        #self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        #self.panedwindow.paneconfigure(self.top_frame, height=50)
        #self.top_frame.config(height=h)
        #self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        #self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)

    def __init__(self, parent, appClass):
        tk.Frame.__init__(self, parent, height=myFrameHeight, width=myFrameWidth)

        self.noOfLinesAllowed=5000.0
        self.stopAutoScroll = False
        self.timeCalledDB = 0

        #btBackgroundColor = '#362F2F'
        btBackgroundColor = '#f0a30a'
        # main frames

        self.panedwindow = tk.PanedWindow(self, orient=tk.VERTICAL, showhandle = True, height=myFrameHeight, width=myFrameWidth)
        self.panedwindow.pack(fill=tk.BOTH, expand=True)

        self.top_frame = tk.Frame(self.panedwindow, background='white', height=(myFrameHeight)*0.7,width=myFrameWidth,  highlightthickness=0, relief=tk.FLAT)
        self.bottom_frame = tk.Frame(self.panedwindow, background='white', width=myFrameWidth,  highlightthickness=0, relief=tk.FLAT)
        self.top_frame.pack_propagate(0)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.bottom_frame.pack_propagate(0)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.panedwindow.add(self.top_frame)
        self.panedwindow.add(self.bottom_frame)

        # Button Frame in top frame
        Frame2 = tk.Frame(self.top_frame,  highlightthickness=0, relief=tk.FLAT)
        Frame2.configure(borderwidth="3")
        Frame2.configure(background=btBackgroundColor)
        Frame2.configure(highlightbackground=btBackgroundColor)
        Frame2.configure(highlightcolor=btBackgroundColor)
        Frame2.pack(side=tk.RIGHT, fill=tk.BOTH,  padx=0, pady=0)

        # right buttons in top frame
        ButtonSaveReceived = Metro_Button(Frame2,text="Save To File", command=lambda: self.ButtonSaveReceived_click(appClass), background=btBackgroundColor)
        ButtonSaveReceived.config(width=12)
        ButtonSaveReceived.pack()

        self.ButtonToggleScroll = Metro_Button(Frame2,text="Stop", command=lambda: self.ButtonChangeAutoScroll_click(appClass), background=btBackgroundColor)
        self.ButtonToggleScroll.config(width=12)
        self.ButtonToggleScroll.pack()

        self.ButtonBack1 = Metro_Button(Frame2,text="Back To Main", command=lambda: self.ButtonBackToMain_click(appClass), background=btBackgroundColor)
        self.ButtonBack1.config(width=12)
        self.ButtonBack1.pack(side=tk.BOTTOM)


        # scrolled text box used to display the serial data
        # Vertical (y) Scroll Bar
        ScrolltxtConsoleRecu = tk.Scrollbar(self.top_frame,  highlightthickness=0, relief=tk.FLAT)
        ScrolltxtConsoleRecu.pack(side=tk.RIGHT, fill=tk.Y)
        # Text Widget
        self.txtConsoleRecu = tk.Text(self.top_frame, width=1, height=1, yscrollcommand=ScrolltxtConsoleRecu.set,  highlightthickness=0, relief=tk.FLAT)
        self.txtConsoleRecu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        # Configure the scrollbars
        ScrolltxtConsoleRecu.config(command=self.txtConsoleRecu.yview)


        # bottom box L and R
        self.bottom_frame_L = tk.Frame(self.bottom_frame, background='white', height=1,width=1,  highlightthickness=0, relief=tk.FLAT)
        self.bottom_frame_R = tk.Frame(self.bottom_frame, background='white', height=1,width=1,  highlightthickness=0, relief=tk.FLAT)
        self.bottom_frame_R.pack(side = tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.bottom_frame_L.pack(side = tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.bottom_frame_L.pack_propagate(0)
        self.bottom_frame_R.pack_propagate(0)


        # box left bottom
        # Vertical (y) Scroll Bar
        ScrollTxtRecu = tk.Scrollbar(self.bottom_frame_L,  highlightthickness=0, relief=tk.FLAT)
        ScrollTxtRecu.pack(side=tk.RIGHT, fill=tk.Y)
        # Text Widget
        self.txtRecu = tk.Text(self.bottom_frame_L, wrap=tk.NONE,  yscrollcommand=ScrollTxtRecu.set,  highlightthickness=0, relief=tk.FLAT)
        self.txtRecu.pack(side=tk.LEFT,  fill=tk.BOTH, expand=True, padx=0, pady=0)
        # Configure the scrollbars
        ScrollTxtRecu.config(command=self.txtRecu.yview)

        # box rigth bottom which includes the sent data
        ScrollTxtSend = tk.Scrollbar(self.bottom_frame_R,  highlightthickness=0, relief=tk.FLAT)
        ScrollTxtSend.pack(side=tk.RIGHT,  fill=tk.Y)
        # Text Widget
        self.txtSend = tk.Text(self.bottom_frame_R, wrap=tk.NONE,  yscrollcommand=ScrollTxtRecu.set,  highlightthickness=0, relief=tk.FLAT)
        self.txtSend.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        # Configure the scrollbars
        ScrollTxtSend.config(command=self.txtSend.yview)

        self.txtSend.bind('<Double-Button-1>', self.SendDBClick)
        self.bind("<Configure>", self.configureEvent)

        self.txtSend.insert(tk.END, '\n')
        self.txtSend.insert(tk.END, 'Help\n')
        self.txtSend.insert(tk.END, 'Auto\n')
        self.txtSend.insert(tk.END, 'Manual\n')
        self.txtSend.insert(tk.END, 'History\n')
        self.txtSend.insert(tk.END, 'Bat\n')
        self.txtSend.insert(tk.END, 'Error\n')
        self.txtSend.insert(tk.END, 'Reset\n')



    def OnReceiveSerialData(self,dataObj):

        if not self.stopAutoScroll:

            # print out expanded list for debugging
            if dataObj.receivedMessage[:1] == '$':  # the first digit is $ then print to txtRecu
                self.txtRecu.insert('1.0', time.strftime("%X ") + dataObj.receivedMessage + '\n')
                #self.txtRecu.insert(tk.END, '\n' + dataObj.receivedMessage )
                #self.txtRecu.insert(tk.END, "Split:\r\n")
                #for item in dataObj.recievedList:
                #    self.txtRecu.insert(tk.END,  "->  " + item + "\r\n")
                lines = float(self.txtRecu.index('end'))
                #delta = lines - self.noOfLinesAllowed
                if lines > self.noOfLinesAllowed:
                    self.txtRecu.delete(self.noOfLinesAllowed+1, 'end')
                    #self.txtRecu.delete('1.0', delta + 1)
                #self.txtRecu.see(tk.END)
            else: # the first digit is not $  then print to txtConsoleRecu
                self.txtConsoleRecu.insert('1.0', time.strftime("%X ") + dataObj.receivedMessage + '\n')
                #self.txtConsoleRecu.insert(tk.END, '\n' + dataObj.receivedMessage )
                lines = float(self.txtConsoleRecu.index('end'))
                #delta = lines - self.noOfLinesAllowed
                if lines > self.noOfLinesAllowed:
                    self.txtConsoleRecu.delete(self.noOfLinesAllowed+1, 'end')
                    #self.txtConsoleRecu.delete('1.0', delta+1)
                #self.txtConsoleRecu.see(tk.END)



