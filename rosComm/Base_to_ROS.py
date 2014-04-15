#!/usr/bin/env python 
# Program to listen to requests from the base station and report back the requested information.
# Derrick Hargwood & Apratim Mukherjee
# 3/23/14
# Rev 3
#Goal: Uses a function called 'listener' to listen to requests from the base station, gathers the information from ROS and sends it back to the base station

import time, serial, rospy, link, listener, re, math


# Initializes link and sets tranmission state to 1
linker = serial.Serial("/dev/ttyUSB0", baudrate = 115200)

listener = listener.listen()
#linker.start()
start = time.time()


class robot():
	def __init__(self):
		self.state = 3
		self.tele_auto = 0
		self.alive = 1
		self.powerlap = 1

robot = robot()

# Reads line from link's rx buffer
def checkBuff():
	
	recievedline = ""
	if linker.inWaiting():
		print 'In loop'
		recievedline = linker.readline().rstrip('\n')
		#if not '\n' in recievedline: return
		code = recievedline.split(' ')
		rCode = code[0]
		data = code[1:]
		actOnRx(rCode,data)
		recievedline = ""
		print rCode, data
		
# Based on state and R-Code recieved, send appropriate R-Code and information back			
def actOnRx(rCode,data):	
	
	if rCode == 'R00': # Keep Alive
		robot.alive = 1
		
	elif rCode == 'R01': # Kill
		robot.alive = 0
		
	elif rCode == 'R02': # Power Down Laptop
		robot.powerlap = 0
		return
	elif rCode == 'R05': # Tele-op
		robot.tele_auto = 0
		 
	elif rCode == 'R06': # Autonomous
		robot.tele_auto = 1
		
	elif rCode == 'R08': # State
		robot.state = int(data[0])
		print 'Changed state to: ',robot.state

	elif rCode == 'R35': # Left Speed Assigned
		robot.lspeed = data

	elif rCode == 'R36': # Right Speed Assigned
		robot.rspeed = data

def Speed():
	r = 0.3937 # [m] Distance from the center of the robot to the center of the wheel 

	if robot.teleauto == 0: # If robot is in tele-op
		return (robot.lspeed, robot.rspeed)
	elif robot.teleauto == 1: # If robot is in autonomous
		vx = listener.twist.linear.x
		wz = listener.twist.angular.z
		delta = wz*r
		lspeed = vx-delta
		rspeed = vs+delta
		return (lspeed, rspeed)
															
# Sends R-Code to links tx buffer		
def sendCode():
	"""TO DO: define all of the send codes to return correct information"""
	print type(robot.state)
	#State 1
	linker.write('prime,R00\n')
	if robot.state == 1: return
	
	declination = 12
	
	if listener.magne.y > 90:
		heading = 90 - math.atan(listener.magne.x/listener.magne.y)*(180/math.pi)
	elif listener.magne.y < 90:
		heading = 270 - math.atan(listener.magne.x/listener.magne.y)*(180/math.pi)
	elif listener.magne.y == 0:
		if listener.magne.x > 0:
			heading = 0
		elif listner.magne.x < 0:
			heading = 180
	
	heading = heading + declination #if this doesn't work, try heading - declination
				
	#State 2
	linker.write('prime,R07\n{}\n'.format(robot.tele_auto)) #Tele-op or autonomous
	linker.write('prime,R37\n{}\n'.format(listener.twist)) 
	linker.write('prime,R53\n{}\n'.format(heading)) #Heading should come from IMU. This needs to change.
	if robot.state == 2: return

	#State 3
	linker.write('prime,R60\n{}\n'.format(listener.left)) #Need rangefinder info
	linker.write('prime,R61\n{}\n'.format(listener.center)) #Need rangefinder info
	linker.write('prime,R62\n{}\n'.format(listener.right)) #Need rangefinder info
	linker.write('prime,R16\n{}\n'.format(time.time()-start)) #Uptime
	if robot.state == 3: return

	#State 4
	linker.write('prime,R40\n{}\n{}\n'.format(listener.lat, listener.lon))   #position from GPS
	#linker.write('prime,R26 ', ['Need more', 'Need more'])   #current waypoint
	#linker.write('prime,R41 ', ['Not available'])      #accuracy of position
	linker.write('prime,R42\n{}\n'.format(listener.numSat))  #Number of satellites
	if robot.state == 4: return
	return
	#State 5
	jpg = open('/home/optimus/Pictures/Webcam/2014-02-23-001737.jpg', 'r').read()
	linker.write('prime,R70\n{}'.format(jpg))
	if robot.state == 5: return
	
# And so it begins...*dramatic background music*
def main():
	
	while not rospy.is_shutdown():
		checkBuff()
		sendCode()
		#time.sleep(1)
		#This function sends data to the transmitter buffer		
print 'Calling main'

try:
	main()
except KeyboardInterrupt:
	linker.stop()
