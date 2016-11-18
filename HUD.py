# -*- coding: utf-8 -*-
import Tkinter as tk
import PIL
import obd
import tkFont
import time

class HUD(tk.Tk):
	def __init__(self,*arg,**kwargs):
		tk.Tk.__init__(self, *arg, **kwargs)
		self.counter = 0
		self.Time = time.time()
		self.overrideredirect(True)
		self.attributes("-fullscreen",True)
		self.configure(background="black")
		self.fillColor = "White"
		self.TextColor = "White"
		self.height=self.winfo_screenheight()
		self.width=self.winfo_screenwidth()
		self.lineWidth = self.height/64
		self.rpmLineStart = self.width/16
		self.rpmLineEnd = self.width/4
		self.mphLineStart = 15*self.width/16
		self.mphLineEnd = 3*self.width/4
		self.tempLineStart = self.height-self.height*5/8
		self.tempLineEnd = self.height/2
		self.font = tkFont.Font(family="Helvetica",size=(self.height+self.width)/18,weight="bold")
		self.canvas = tk.Canvas(self,width=self.width,height=self.height,highlightthickness=0)
		self.canvas.configure(background="Black")
		self.canvas.pack(fill="both", expand=True)
		self.RPM = connection.query(cmdRPM)
		self.SPEED = connection.query(cmdSPEED)
		self.TEMP = connection.query(cmdTEMP)
		self.RPMLABEL = self.canvas.create_text(self.width/2,self.height-3*self.height/8,text="° F",font=self.font,fill="white",tag="text")
		self.MPHLABEL = self.canvas.create_text(self.width/2,self.height-self.height/4,text="MPH",font=self.font,fill="white",tag="text")
		self.TEMPLABEL = self.canvas.create_text(self.width/2,self.height-self.height/8,text="RPM",font=self.font,fill="white",tag="text")
		self.Sanitize()
		self.Update()

	def Sanitize(self):
		if str(self.RPM).partition(" ")[0] == "None":
			self.RPM = 0
		if str(self.SPEED).partition(" ")[0] == "None":
			self.SPEED = 0
		else:
			self.SPEED = self.SPEED/1.609344 #converts KMH to MPH
		if str(self.TEMP).partition(" ")[0] == "None":
			self.TEMP = 32
		else:
			self.TEMP = ((self.TEMP*9)/5)+32

	def Read(self):
		self.RPM = connection.query(cmdRPM)
		self.SPEED = connection.query(cmdSPEED)
		self.TEMP = connection.query(cmdTEMP)

	def Update(self):
		self.Read()
		self.Sanitize()
		self.canvas.delete("text")
		self.canvas.delete("line")
		#self.TEMP = 240.23
		#self.SPEED = 75.23
		#self.RPM = 3200.23
		if(self.RPM == 0 ):
			self.fillColor = "Red"
			self.canvas.create_line(self.rpmLineStart,self.height-self.height/32,self.rpmLineEnd, self.height-self.height/32, fill=self.fillColor,width=self.lineWidth,tag='line')
			self.canvas.create_text(self.width/2,self.height-self.height/8,text="< " + str(int(self.RPM))+" RPM",font=self.font,fill=self.TextColor,tag="text")
		else:
			if self.RPM < 2000:
				self.fillColor = "White"
			elif self.RPM >= 2000 and self.RPM < 4000:
				self.fillColor = "Yellow"
			else:
				self.fillColor = "Red"
			for x in range(1,int(self.RPM/250)):
				self.canvas.create_line(self.rpmLineStart,self.height-self.height*x/32,self.rpmLineEnd,self.height-self.height*x/32, fill = self.fillColor, width=self.lineWidth,tag='line')
			self.canvas.create_text(self.width/2,self.height-self.height/8,text="< " + str(int(self.RPM))+" RPM",font=self.font,fill=self.TextColor,tag="text")	
		if(self.SPEED == 0):
			self.fillColor = "Red"
			self.canvas.create_line(self.mphLineStart,self.height-self.height/32,self.mphLineEnd,self.height-self.height/32,fill=self.fillColor,width=self.lineWidth,tag='line')
			self.canvas.create_text(self.width/2,self.height-self.height/4,text=str(int(self.SPEED))+ " MPH >",font=self.font,fill=self.TextColor,tag="text")
		else:
			if self.SPEED < 80:
				self.fillColor = "White"
			elif self.SPEED >= 80 and self.SPEED < 90:
				self.fillColor = "Yellow"
			else:
				self.fillColor = "Red"
			for x in range(1,int(self.SPEED/6.25)):
				self.canvas.create_line(self.mphLineStart,self.height-self.height*x/32,self.mphLineEnd,self.height-self.height*x/32,fill=self.fillColor,width=self.lineWidth,tag='line')
			self.canvas.create_text(self.width/2,self.height-self.height/4,text=str(int(self.SPEED))+" MPH >",font=self.font,fill=self.TextColor,tag="text")
		if(self.TEMP == 32):
			self.fillColor = "Red"
			self.canvas.create_line(self.width*24/52,self.tempLineStart,self.width*24/52,self.tempLineEnd,fill=self.fillColor,width=self.lineWidth)
			self.canvas.create_text(self.width/2,self.height-3*self.height/8,text=str(int(self.TEMP))+"° F",font=self.font,fill=self.TextColor,tag="text")
		else:
			if self.TEMP < 185:
				self.fillColor = "White"
			elif self.TEMP >= 185 and self.TEMP < 230:
				self.fillColor = "Yellow"
			else:
				self.fillColor = "Red"
			for x in range(1,int(self.TEMP/28.5)):
				self.canvas.create_line(self.width*(24+x)/52,self.tempLineStart,self.width*(24+x)/52,self.tempLineEnd,fill=self.fillColor,width=self.lineWidth)
			self.canvas.create_text(self.width/2,self.height-3*self.height/8,text=str(int(self.TEMP))+ "° F",font=self.font,fill=self.TextColor,tag="text")
		print("Time:" + str(time.time()-self.Time) + " - Number of Loops: " + str(self.counter))
		self.counter = self.counter + 1
		self.after(25,self.Update)
		



connection = obd.Async()
cmdRPM = obd.commands.RPM
cmdSPEED = obd.commands.SPEED
cmdTEMP = obd.commands.COOLANT_TEMP
connection.watch(cmdRPM,force=True)
connection.watch(cmdSPEED,force=True)
connection.watch(cmdTEMP,force=True)
myHUD=HUD()
myHUD.mainloop()		