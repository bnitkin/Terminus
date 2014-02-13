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
	tmp = ''	#Data 
	
	txRate = 10000 #Force high to avoid disabled widgets in demo mode.
	rxRate = 10000
	
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
		clock = time.Clock()
		#Rolling averages for d(data)/d(time) for tx and rx
		txData = deque(maxlen=RATE_AVG)
		txTime = deque((0, 1), maxlen=RATE_AVG) #(0, 1) prevents div/0 errors
		rxData = deque(maxlen=RATE_AVG)
		rxTime = deque((0, 1), maxlen=RATE_AVG)

		while self.alive:
			waiting = self.ser.inWaiting()
			#RX data from PySerial buffer
			if waiting:
				#Keep statistics on reception data rate.
				rxData.append(waiting)
				rxTime.append(time.get_ticks())
				
				#Check buffer and warn of possible data loss.
				if waiting > 3000: sys.stderr.write("!! Warning: buffer nearly full ({}B of3900B max).\n".format(waiting))
			
				line = 'this is not blank'
				while line != '':
					line = self.ser.readline(self.ser.inWaiting())
					self.rx.append(line)
					
			#Transmit data once buffer's full, but for no longer than TIMEOUT. 
			start = time.get_ticks()
			while len(self.tx) and (time.get_ticks() - start) < TIME_WRITE: #Transmit for no longer than timeout
				#Keep statistics on transmission data rate.
				txData.append(len(self.tx[0]))
				txTime.append(time.get_ticks())
			
				print '#' + self.tx[0]
				self.ser.write(self.tx.popleft())
					
			self.txRate = 1000 * sum(txData) / (txTime[-1]-txTime[0])
			self.rxRate = 1000 * sum(rxData) / (rxTime[-1]-rxTime[0])

			#Limit framerate by TIME_MIN.
			clock.tick(1000/TIME_MIN)
	
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
		return self.rx.popleft(0)
		
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
			line = readLine()
			if line.startswith('prime'): 
				#Starting read now.
				if code == '': code = line[6:-1] #Clip the 'prime,' and '\n'
				#Hit another code; we're done reading. Push the last line back into the buffer and return.
				else: 
					self.rx.insert(0, line)
					return code, data
			elif code != '': #The line isn't a code and we're recording
				data += line + '\n' #Restore newline to data.
		
	def hasCode(self):
		"""Returns whether there's a full code to read."""
		#XXX Rewrite for R-code slave

		#A complete code requires two 'prime' lines: one to start the code and one to end it.
		codes = 0
		for line in self.rx:
			if line.startswith('prime'): codes += 1
			if codes == 2: return True
		return False
		
	def stop(self): 
		"""Kills the thread."""
		self.alive = False
