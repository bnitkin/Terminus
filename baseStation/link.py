#!/usr/bin/python2
# Jan 2014
# Ben Nitkin
# 
# Serial interface
# Buffers communications to and from the robot to reduce data loss. 
# Serial.write() and Serial.readLine() / .readCode() send and recieve data. 

import serial, threading, sys
from pygame import time
from config import *

import pygame
pygame.init()

class Serial(threading.Thread):	
	tx = []	# List of strings to transmit. The manager automatically appends newlines.
	rx = []	# List of recieved lines (newline stripped)
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
		txData = [0]*RATE_AVG
		txTime = [0]*(RATE_AVG-1) + [1] #Prevents div/zero errors.
		rxData = [0]*RATE_AVG
		rxTime = [0]*(RATE_AVG-1) + [1]
		
		while self.alive:
			waiting = self.ser.inWaiting()
			#Recieve data from PySerial buffer
			if waiting:
				#Keep statistics on transmission data rate.
				del rxData[0]
				rxData.append(waiting)
				del rxTime[0]
				rxTime.append(time.get_ticks())
				
				if waiting > 3000: sys.stderr.write("!! Warning: buffer nearly full ({}B of3900B max).\n".format(waiting))
				self.tmp += self.ser.read(self.ser.inWaiting())
				print self.tmp
				#Once a newline's detected, push the line to rx[]
				lines = self.tmp.splitlines()
				if len(lines) > 1: #We have a full line to push to cache.
					if self.tmp[-1] == '\n': #Push all completed lines to cache
						self.rx += lines
						self.tmp = ''
					else: #The last line is incomplete; leave it in self.tmp.
						self.rx += lines[:-1]
						self.tmp = lines[-1]
						
			#Transmit data once buffer's full, but for no longer than TIMEOUT. 
			start = time.get_ticks()
			while len(self.tx) and (time.get_ticks() - start) < TIME_WRITE:
				#Keep statistics on transmission data rate.
				del txData[0]
				txData.append(len(self.tx[0])+1) #Add the newline.
				del txTime[0]
				txTime.append(time.get_ticks())
				
				print '#' + self.tx[0]
				self.ser.write(self.tx.pop(0)+'\n')

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
		return self.rx.pop(0)
		
	def write(self, data):
		"""Writes a string to the transmission buffer"""
		self.tx.append(data)
		
	def readCode(self):
		"""Reads a full code from the recieved buffer"""
		#Return the first line in the buffer stopping before the next code begins.
		#TODO: Define codes.
		#Return: (code, data (newline delimited, again)
		pass
		
	def hasCode(self):
		"""Returns whether there's a full code to read."""
		#TODO
		return False
		pass
	
	def stop(self): 
		"""Kills the thread."""
		self.alive = False
