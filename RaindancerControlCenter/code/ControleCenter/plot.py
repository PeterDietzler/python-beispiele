#!/usr/bin/python
#
# Read stream of lines from an Arduino with a magnetic sensor. This
# produces 3 values per line every 50ms that relate to the orientation
# of the sensor. Each line looks like:
# MAG   1.00    -2.00   0.00
# with each data line starting with "MAG" and each field separated by
# tab characters. Values are floating point numbers in ASCII encoding.
#
# This script supports both Python 2.7 and Python 3
# https://arduino.stackexchange.com/questions/17486/graph-plotting-on-python-using-tkinter-canvas



import tkinter as tk
import math
from globalvars import myFrameHeight
from globalvars import myFrameWidth

class TPlot(tk.Frame):
    # _bufferPoint how many samples will be stored. This samples will be shown from left side to right side of the window
    # _noOfCharts How many charts will be used: 1,2 or 3
    # _refreshrate after how much new inserted samples the chart should be drawn. Minimal value is 1. Then after each inserted value the chart is drwan.
    def __init__(self, parent, title, _bufferPoints, _noOfCharts, _refreshrate):
        tk.Frame.__init__(self, parent) #, height=myFrameHeight/2, width=myFrameWidth
        self.npoints = _bufferPoints
        self.noOfCharts = _noOfCharts
        self.refreshrate = _refreshrate

        self.canvas = tk.Canvas(self, background="white", height=1, width=1) #, height=myFrameHeight/2, width=myFrameWidth
        self.canvas.bind("<Configure>", self.on_resize)

        self.zeroLine = self.canvas.create_line((0, 0, 0, 0), fill='grey64', width=1)

        self.LineA = [0 for x in range(self.npoints)]
        self.canvas.create_line((0, 0, 0, 0), tag='A', fill='blue', width=1)
        self.objIdTextCurrentA = self.canvas.create_text(5, 30, anchor="w", text="Min:", fill="blue")

        if self.noOfCharts > 1:
            self.LineB = [0 for x in range(self.npoints)]
            self.canvas.create_line((0, 0, 0, 0), tag='B', fill='red', width=1)
            self.objIdTextCurrentB = self.canvas.create_text(5, 40, anchor="w", text="Min:", fill="red")

        if self.noOfCharts > 2:
            self.LineC = [0 for x in range(self.npoints)]
            self.canvas.create_line((0, 0, 0, 0), tag='C', fill='green', width=1)
            self.objIdTextCurrentC = self.canvas.create_text(5, 50, anchor="w", text="Min:", fill="green")


        self.canvas.pack(side="top", fill="both", expand=True)

        #self.canvas.grid(sticky="news")
        #self.grid_rowconfigure(0, weight=0)
        #self.grid_columnconfigure(0, weight=0)
        #self.grid(sticky="news")

        self.objIdTextMax = self.canvas.create_text(5, 10, anchor="w", text="Max:", fill="red")
        self.objIdTextMin = self.canvas.create_text(5, 10, anchor="w", text="Min:", fill="red")

        self.count = 0

    def on_resize(self, event):
        self.replot()

    def deleteBuffer(self):
        self.LineA = [0 for x in range(self.npoints)]
        if self.noOfCharts > 1:
            self.LineB = [0 for x in range(self.npoints)]
        if self.noOfCharts > 2:
            self.LineC = [0 for x in range(self.npoints)]

    def addPlotData(self, x, y, z):
        """
        Update the cached data lists with new sensor values.
        """
        self.LineA.append(float(x))
        #print(len(self.LineA))
        #self.LineA = self.LineA[-1 * self.npoints:]
        self.LineA.pop(0)
        #print(len(self.LineA))

        if self.noOfCharts > 1:
            self.LineB.append(float(y))
            #self.LineB = self.LineB[-1 * self.npoints:]
            self.LineB.pop(0)
        if self.noOfCharts > 2:
            self.LineC.append(float(z))
            #self.LineC = self.LineC[-1 * self.npoints:]
            self.LineC.pop(0)

        self.count += 1

        # Registers a callback that is called when the system is idle. The callback will be called there are no more events to process in the mainloop.
        if math.fmod(int(self.count), int(self.refreshrate)) == 0:
            self.after_idle(self.replot)
            #self.after(1, self.replot)

        return

    def replot(self):
        """
        Update the canvas graph lines from the cached data lists.
        The lines are scaled to match the canvas size as the window may
        be resized by the user.
        Canvas uppler left corner is 0,0
        """
        w = self.winfo_width()
        h = self.winfo_height()
        coordsA, coordsB, coordsC = [], [], []

        # get the highest and lowest value
        max_A = max(self.LineA)
        min_A = min(self.LineA)

        if self.noOfCharts > 1:
            max_B = max(self.LineB)
            min_B = min(self.LineB)
            if max_B > max_A:
                max_A = max_B
            if min_B < min_A:
                min_A = min_B

        if self.noOfCharts > 2:
            max_C = max(self.LineC)
            min_C = min(self.LineC)
            if max_C > max_A:
                max_A = max_C
            if min_C < min_A:
                min_A = min_C

        # check if we have a horizontal line:
        delta = (max_A - min_A)
        if delta == 0:
            if max_A > 0:
                min_A = max_A * -0.1
            elif max_A < 0:
                max_A = max_A * -0.1
            else:
                max_A = 1
                min_A = -1
        elif max_A == 0:
                max_A = min_A * -0.1  # we want to see the zero line
        elif min_A == 0:
                min_A = max_A * -0.1  # we want to see the zero line

        max_A_saved = max_A
        min_A_saved = min_A

        max_A *= 1.05  # increase the max/min to have space between graph and border
        min_A *= 1.05
        delta = (max_A - min_A) # calculate delta again because of changed max/min values

        x_scale = w / self.npoints
        y_scale = h / delta
        zeroPosition = h - (y_scale * (0 - min_A))

        for n in range(0, self.npoints):
            x = x_scale * n   # (w * n) / self.npoints
            # chart A
            coordsA.append(x)
            y = h - (y_scale * (self.LineA[n]-min_A))
            coordsA.append(y)

            # chart B
            if self.noOfCharts > 1:
                coordsB.append(x)
                y = h - (y_scale * (self.LineB[n] - min_A))
                coordsB.append(y)

            # chart C
            if self.noOfCharts > 2:
                coordsC.append(x)
                y = h - (y_scale * (self.LineC[n] - min_A))
                coordsC.append(y)

        self.canvas.coords('A', *coordsA)
        if self.noOfCharts > 1:
            self.canvas.coords('B', *coordsB)
        if self.noOfCharts > 2:
            self.canvas.coords('C', *coordsC)

        # zero line
        coordsZeroLine = (0, zeroPosition, w, zeroPosition)
        self.canvas.coords(self.zeroLine, *coordsZeroLine)

        # current Text
        text = "Cur: " + "%.2f" % self.LineA[-1]
        self.canvas.itemconfig(self.objIdTextCurrentA, text=text)
        if self.noOfCharts > 1:
            text = "Cur: " + "%.2f" % self.LineB[-1]
            self.canvas.itemconfig(self.objIdTextCurrentB, text=text)
        if self.noOfCharts > 2:
            text = "Cur: " + "%.2f" % self.LineC[-1]
            self.canvas.itemconfig(self.objIdTextCurrentC, text=text)

        # max text
        text = "Max: " + "%.2f" % max_A_saved
        self.canvas.itemconfig(self.objIdTextMax, text=text)

        # min text
        text = "Min: " + "%.2f" % min_A_saved
        self.canvas.itemconfig(self.objIdTextMin, text=text)
        coordsMinText = (5, h-10)
        self.canvas.coords(self.objIdTextMin, *coordsMinText)



