# Tab Host
from printrun.printcore import printcore
from printrun import gcoder

import sys
import time
import os


class tabHost():
	
	baud = "57600"
	port = "COM8"
	
	pCore = None
	gCode = None
	
	loud = False
	repStat = True

	def __init__(self, port=None, baund=None):
		if port is not None:
			self.port = port
		
		if baund is not None:
			self.bound = baund
	
	def connect(self):
		
		if self.repStat == True:
			sys.stdout.write("Connecting to TaB:")
			sys.stdout.flush()
		
		self.pCore = printcore(self.port, self.baud)
		while self.pCore.online == False:
			time.sleep(1)
			if self.repStat == True:
				sys.stdout.write(".")
				sys.stdout.flush()
		
		if self.repStat == True:
			sys.stdout.write("Tab conneceted!\n")
			
		self.pCore.loud = self.loud
		time.sleep(2)
		
	def postProcess(self, msg = None, gCodeFile = None):
		
		if msg is not None:
			pass
		elif gCodeFile is not None:
			if os.path.exists(gCodeFile):
				self.gCode = [i.strip() for i in open(gCodeFile)]
				self.gCode = gcoder.LightGCode(self.gCode)
			else:
				print("File %s does not exists!" %(gCodeFile) )
		else:
			print("At least one among msg or g-code file must be not none.")
			
		
	def run(self):
		if self.pCore is None:
			print("Connect the TaB before running")
			return
		
		if self.gCode is None:
			print("Post-process a string or give a G-Code file before running")
			return
		
		# Avvio la stampa
		self.pCore.startprint(self.gCode)
		
		try:
			if self.repStat == True:
				self.pCore.loud = self.loud
				sys.stdout.write("Progress: 00.0%\r")
				sys.stdout.flush()
			while self.pCore.printing:
				time.sleep(1)
				if self.repStat == True:
					progress = 100 * float(self.pCore.queueindex) / len(self.pCore.mainqueue)
					sys.stdout.write("Progress: %02.1f%%\r" % progress)
					sys.stdout.flush()
			self.pCore.disconnect()
		except:
			self.pCore.disconnect()