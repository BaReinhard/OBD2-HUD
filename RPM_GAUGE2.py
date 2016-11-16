import Tkinter as tk
import math
import time
import obd
import os, sys
import random
import tkFont
from PIL import Image


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class TachoMeter(tk.Tk):
    def __init__(self, CenterPoint=Point(), LeftPoint=Point(), Radius=0, LeftBuffer=0, BottomBuffer=0, MIN_RPM=0,
                 MAX_RPM=0, canvas_height=0, canvas_width=0, *arg, **kwargs):
        tk.Tk.__init__(self, *arg, **kwargs)
        self.canvas = tk.Canvas()
        self.canvas.configure(width=self.canvas.winfo_screenwidth(), height=self.canvas.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.CenterPoint = CenterPoint
        self.MAX_RPM = MAX_RPM
        self.MIN_RPM = MIN_RPM
        self.LeftBuffer = LeftBuffer
        self.BottomBuffer = BottomBuffer
        self.Radius = Radius
        self.Point_0 = LeftPoint
        self.photo = tk.PhotoImage(file = "/Users/Brett/Desktop/RPM_GAUGE/GaugeBackground.gif")
        self.canvas.create_image(500,275, image=self.photo)
        self.canvas.create_oval(self.CenterPoint.x-8,self.CenterPoint.y-8,self.CenterPoint.x+8,self.CenterPoint.y+8, fill="Red", outline="Red")
        self.canvas.configure(background="Black")
        #self._create_arc((LeftPoint.x, LeftPoint.y), (LeftPoint.x + 2 * Radius, LeftPoint.y))
        self.angle = float(0)
        self.speed = str(connection.query(obd.commands.SPEED)).partition(" ")[0]
        self.line = -1
        self.font = tkFont.Font(family='Helvetica',size=36, weight='bold')
        self.RPM_LABEL = self.canvas.create_text(self.CenterPoint.x+self.Radius,self.CenterPoint.y+self.BottomBuffer/4, fill="White", font=self.font)
        self.canvas.itemconfigure(self.RPM_LABEL, text = "RPM")
        self.SPEED_LABEL = self.canvas.create_text(self.Point_0.x+40,self.Point_0.y+self.BottomBuffer/4, fill = "White", font=self.font)
        self.canvas.itemconfigure(self.SPEED_LABEL, text = "SPEED MPH")
        self.RPM_TEXT = self.angle
        self.RPM_OBJECT = -1
        self.SPEED_TEXT = self.speed
        self.SPEED_OBJECT = -1
        self._rpmGauge()

    def _create_arc(self, p0, p1):
        extend_x = (self._distance(p0, p1) - (p1[0] - p0[0])) / 2
        extend_y = (self._distance(p0, p1) - (p1[1] - p0[1])) / 2
        theta = p0[0] - p1[0], p0[1] - p1[1] * 180 / math.pi
        startAngle = math.atan2(p0[0] - p1[0], p0[1] - p1[1]) * 180 / math.pi
        if (theta == (math.pi)/2):
            rpm4000 = self.canvas.create_text(p0,p1)
            self.canvas.itemconfigure(rpm4000,text = "4000")
        self.canvas.create_arc(p0[0] - extend_x, p0[1] - extend_y, p1[0] + extend_x, p1[1] + extend_y, extent=180,
                               start=90 + startAngle)
        #self.canvas.create_arc(LeftPoint.x + Radius, LeftPoint.y, LeftPoint.x + Radius, LeftPoint.y - Radius)

    def _distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)

    def _rpmGauge(self):
        #randomNumber = random.uniform(0,8000)
        if (str(self.angle).partition(" ")[0] =="None"):
            self.angle = 0
        curTheta = float((math.pi * ((self.MAX_RPM-self.angle)/self.MAX_RPM)))
        curX = self.CenterPoint.x + (self.Radius * math.cos(curTheta))
        curY = self.CenterPoint.y - (self.Radius * math.sin(curTheta))
        self.canvas.delete(self.line)
        self.canvas.delete(self.RPM_OBJECT)
        self.canvas.delete(self.SPEED_OBJECT)
        self.line = self.canvas.create_line(self.CenterPoint.x, self.CenterPoint.y, int(curX), int(curY),width=10,fill="Red")
        self.RPM_OBJECT = self.canvas.create_text(self.CenterPoint.x+self.Radius,self.CenterPoint.y + self.BottomBuffer/2 + 25,fill="White", font=self.font)
        self.SPEED_OBJECT = self.canvas.create_text(self.Point_0.x+40,self.Point_0.y + self.BottomBuffer/2 + 25, fill = "White", font=self.font)
        self.RPM_TEXT = int(self.angle)#randomNumber)#self.angle
        self.SPEED_TEXT = self.speed
        self.canvas.itemconfigure(self.RPM_OBJECT, text = self.RPM_TEXT)
        self.canvas.itemconfigure(self.SPEED_OBJECT, text= self.SPEED_TEXT)
        self.canvas.pack()
        self.angle = connection.query(cmd)
        if (str(self.angle).partition(" ")[0]=="None"):
            self.angle=0
        
        self.angle = float(str(self.angle).partition(" ")[0])
        self.speed = str(connection.query(obd.commands.SPEED)).partition(" ")[0]
        
        self.after(155, self._rpmGauge)

#pilImage = Image.open("/Users/Brett/Desktop/RPM_GAUGE/GaugeBackground.gif")

Radius = 400
connection = obd.Async()
cmd = obd.commands.RPM
connection.watch(cmd,force=True)
connection.watch(obd.commands.SPEED,force=True)
connection.start()
acanvas_width = 1000
acanvas_height = 600
LeftBuffer = 100
BottomBuffer = 100
CenterPoint = Point(LeftBuffer + Radius, acanvas_height - BottomBuffer)
LeftPoint = Point(LeftBuffer, acanvas_height - BottomBuffer)
MAX_RPM = 8000
MIN_RPM = 0

TACH = TachoMeter(CenterPoint, LeftPoint, Radius, LeftBuffer, BottomBuffer, MIN_RPM, MAX_RPM, acanvas_height,
                  acanvas_width)

TACH.mainloop()