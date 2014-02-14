#!/usr/bin/python2
# Jan 2014
# Ben Nitkin
# 
# Serial interface
# Buffers communications to and from the robot to reduce data loss. 
# Serial.write() and Serial.readLine() / .readCode() send and recieve data. 

import serial, threading, sys
from collections import deque #Fast buffer
from pygame import time
from config import *

import pygame
pygame.init()

class Serial(threading.Thread):	
	tx = deque()	# List of strings to transmit. The manager automatically appends newlines.
	rx = deque()	# List of recieved lines (newline stripped)
	tmp = ''	#Temp buffer for partial recieved lines. 
	
	txRate = 10000 #Force high to avoid disabled widgets in demo mode.
	rxRate = 10000
	
	
	clock = time.Clock()
	#Rolling averages for d(data)/d(time) for tx and rx
	txData = deque(maxlen=RATE_AVG)
	txTime = deque((0, 1), maxlen=RATE_AVG) #(0, 1) prevents div/0 errors
	rxData = deque(maxlen=RATE_AVG)
	rxTime = deque((0, 1), maxlen=RATE_AVG)
	
	alive = True
	#If the serial device isn't accessable, throw a terminal warning but proceed.
	try: 
		ser = serial.Serial(PORT, BAUDRATE, timeout = 0)
	except:
		sys.stderr.write("!! Serial device {} not accessable. Proceeding in demo mode.\n".format(PORT))
		alive = False

	def run(self):
		"""Thread to manage the serial port. 
		Retrieve all data that pyserial's buffered. 
		Push all full lines into the local recieved buffer. Save any partial line in tmp.
		Transmit all queued codes."""

		while self.alive:
			self.recieve()
			self.transmit()
			#Limit framerate by TIME_MIN.
			self.clock.tick(1000/TIME_MIN)

		
	def recieve(self):
		#RX data from PySerial buffer		
		self.rxData.append(self.ser.inWaiting())
		self.rxTime.append(time.get_ticks())
		if self.ser.inWaiting():
			#Keep statistics on reception data rate.
			
			#Check buffer and warn of possible data loss.
			if self.ser.inWaiting() > 3000: sys.stderr.write("!! Warning: buffer nearly full ({}B of ~3900B max).\n".format(self.ser.inWaiting()))
		
			#Read lines into the rx buffer.
			lines = self.ser.read(self.ser.inWaiting()).split('\n')
			
			lines[0] = self.tmp + lines[0] #Append any partial line.
			self.tmp = '' #Clear temp line
			
			self.rx.extend(lines[:-1]) #The last line is either '' or a partial transmission.
			for line in lines[:-1]: print line
			
			if lines[-1] != '': #Last line is incomplete
				self.tmp = lines[-1]
				
	def transmit(self):
		#Transmit data to empty tx buffer, but for no longer than TIMEOUT. 
		start = time.get_ticks()
		while len(self.tx) and ((time.get_ticks() - start) < TIME_WRITE): #Transmit for no longer than timeout
			#Keep statistics on transmission data rate.
			self.txData.append(len(self.tx[0]))
			self.txTime.append(time.get_ticks())
		
			print '#' + self.tx[0],
			self.ser.write(self.tx.popleft())
				
		self.txRate = 1000 * sum(self.txData) / (self.txTime[-1]-self.txTime[0])
		self.rxRate = 1000 * sum(self.rxData) / (self.rxTime[-1]-self.rxTime[0])
	
	#Keep track of sending and recieving speeds, B/s
	def txSpeed(self): return self.txRate
	def rxSpeed(self): return self.rxRate
	def inWaiting(self):
		"""Returns the number of lines in the recieved buffer."""
		return len(self.rx)
		
	def outWaiting(self):
		"""Returns the number of lines in the transmission buffer."""
		return len(self.tx)
		
	def readLine(self):
		"""Reads a single line from the buffer, with the original trailing newline stripped."""
		return self.rx.popleft()
		
	def write(self, data):
		"""Writes a string to the transmission buffer"""
		self.tx.append(data)
	
	def writeCode(self, code):
		"""Adds protocol fiddley bits to codes before writing."""
		#XXX Rewrite for R-code slave
		self.write(code+'\n')
	
	def readCode(self):
		"""Reads a full code from the recieved buffer. 
		Purges any partial code in the buffer."""	
		#XXX Rewrite for R-code slave
		code = ''
		data = ''
		while True:
			line = self.readLine()
			if line.startswith('prime'): 
				#Starting read now.
				if code == '': code = line[6:] #Clip the 'prime,' and '\n'
				#Hit another code; we're done reading. Push the last line back into the buffer and return.
				else: 
					self.rx.appendleft(line)
					return code, data
					
			elif code != '': #The line isn't a code and we're recording
				data += line + '\n' #Restore newline to data.
		
	def hasCode(self):
		"""Returns whether there's a full code to read."""
		#XXX Rewrite for R-code slave

		#A complete code requires two 'prime' lines: one to start the code and one to end it.
		codes = 0
		temprx = list(self.rx)
		for line in temprx:
			if line.startswith('prime'): codes += 1
			if codes == 2: return True
		return False
		
	def stop(self): 
		"""Kills the thread."""
		self.alive = False
