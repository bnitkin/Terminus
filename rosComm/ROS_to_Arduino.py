#!/usr/bin/env python 
# Derrick Hargwood & Apratim Mukherjee
# 4/18/14
# Rev 1
# Goal: Grabs relevant information from Arduino and pipes some of it back to the 
# base station. Also, sets the left and right speeds of the robot's motors.

import serial, time, rospy, link, re
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

#link = serial.Serial('/dev/ttyACM0', baudrate = 9600) #Change port to Arduino's current number 'ACM*'
link = link.Serial()
link.start()
print 'IIII\nIIII\nIIII\nIIII\nIIII\nIIII\nIIII\nIIII\nIIII\nIIII\nIIII\nIIII\nIIII\n'

class Arduino():
	def __init__(self):
		self.left = 0.51 #So the way the base station is set up, it requires at least two digits after the decimal.
		self.right = 0.51
		self.center = 0.51
		self.twistact = (0,0)
		self.twistass = 0 # m/s and rad/s - Might need to publish		
		self.lspeedact = 0 #This is the speed that the arduino reports back to the ROS
		self.rspeedact = 0
		self.lspeedass = 0 #This is the speed that the ROS assigns the arduino
		self.rspeedass = 0
		self.volt = 0
		self.curdraw = 0
		self.avgdraw = 0
		self.tmp = ''

"""
def talker():
     leftpub = rospy.Publisher('LeftRange', Float64)
     rightpub = rospy.Publisher('RightRange', Float64)
     centerpub = rospy.Publisher('CenterRange', Float64)
     twistpub = rospy.Publisher('ActualTwist',Twist)
     
     rospy.init_node('talker', anonymous=True)
"""
ard = Arduino()

def actOnRCode(rCode):
	if rCode == 'R10': # Battery Voltage
		data = float(link.readLine())
		ard.volt = data
	elif rCode == 'R13': # Battery current draw
		data = float(link.readLine())
		ard.curdraw = data
	elif rCode == 'R14': # Battery average current draw
		data = float(link.readLine())
		ard.avgdraw = data
	elif rCode == 'R37': # Actual twist reported from Arduino
		data1 = float(link.readLine())
		data2 = float(link.readLine())
		ard.twistact[0] = data1
		ard.twistact[1] = data2
	elif rCode == 'R38': # Actual left speed reported from Arduino
		data = float(link.readLine())
		ard.lspeedact = data
	elif rCode == 'R39': # Actual right speed reported from Arduino
		data = float(link.readLine())
		ard.rspeedact = data
	elif rCode == 'R60': # Distance from left rangefinder
		data = float(link.readLine())
		ard.left = data
	elif rCode == 'R61': # Distance from right rangefinder
		data = float(link.readLine())
		ard.right = data
	elif rCode == 'R62': # Distance from center rangefinder
		data = float(link.readLine())
		ard.center = data			

# checkBuff: Pulls data from recieve buffer for no longer than TIMEOUT
def checkBuff():

	while link.inWaiting() > 5:
		if 'prime,' in link.previewLine():
			code = link.readLine().split(',')
			rcode = code[1]	
			actOnRCode(rcode)
		else:
			link.readLine()

# sendCode: sends codes to the Arduino.	
def sendCode():
	lspeed = 1 
	rspeed = 1
	#lspeed, rspeed = Base_to_ROS.Speed()
	link.write('prime,R35\n{}\n'.format(lspeed))
	link.write('prime,R36\n{}\n'.format(rspeed))
	
	
# Main function. Starts all of the code.	
def main():
	while not rospy.is_shutdown():
		print 'loop'
		leftpub.publish(ard.left)
		rightpub.publish(ard.right)
		centerpub.publish(ard.center)
		checkBuff()
		sendCode()


leftpub = rospy.Publisher('LeftRange', Float64)
rightpub = rospy.Publisher('RightRange', Float64)
centerpub = rospy.Publisher('CenterRange', Float64)
twistpub = rospy.Publisher('ActualTwist',Twist)
     
rospy.init_node('talker', anonymous=True)
main()
"""
try:
	main()	
except KeyboardInterrupt, k:
	link.stop()
"""
