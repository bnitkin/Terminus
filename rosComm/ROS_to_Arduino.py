#!/usr/bin/env python 
# Program to listen to requests from the base station and report back the requested information.
# Derrick Hargwood & Apratim Mukherjee
# 3/23/14
# Rev 1

import serial, time, rospy, Base_to_ROS

link = serial.Serial('/dev/ttyUSB*', baudrate = 115200) #Change port to Arduino's current number

class Arduino():
	def __init__(self):
		self.left = 0
		self.right = 0
		self.center = 0
		self.twistact = 0
		self.twistass = 0 # m/s and rad/s - Might need to publish		
		self.lspeedact = 0 #This is the speed that the arduino reports back to the ROS
		self.rspeedact = 0
		self.lspeedass = 0 #This is the speed that the ROS assigns the arduino
		self.rspeedass = 0
		self.volt = 0
		self.curdraw = 0
		self.avgdraw = 0

ard = Arduino()

def actOnRCode(rCode,data):
	if rCode == 'R10'
		ard.volt = data
	elif rCode == 'R13'
		ard.curdraw = data
	elif rCode == 'R14'
		ard.avgdraw = data
	elif rCode == 'R37'
		ard.twistact = data
	elif rCode == 'R38'
		ard.lspeedact = data
	elif rCode == 'R39'
		ard.rspeedact = data
	elif rCode == 'R60'
		ard.left = data
	elif rCode == 'R61'
		ard.right = data
	elif rCode == 'R62'
		ard.center = data	
		
def checkBuff():
	timeout = 0.3
	start = time.time()
	while link.inWaiting() and not (time.time() - start) > timeout:
		code = link.readline().split(' ')
		rCode = code[0]
		data = code[1:]
		actOnRCode(rCode,data)
	
def sendCode():
	lspeed, rspeed = Base_to_ROS.Speed()
	link.write('prime,R35\n{}\n'.format(lspeed))
	link.write('prime,R36\n{}\n'.format(rspeed))
	
def main():
	checkBuff()
	sendCode()
