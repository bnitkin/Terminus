#!/usr/bin/env python 
# Program to listen to requests from the base station and report back the requested information.
# Derrick Hargwood & Apratim Mukherjee
# 2/27/14
# Rev 2

# !!!Some things are currently commented out for testing purposes!!!

import time, serial, rospy, link, listener

'''
# Initializes link and sets tranmission state to 1
linker = link.Serial()
linker.run()
listener = listener.listen()
state = 1
'''
listener = listener.listen()
state = 1

# Reads line from link's rx buffer
def readBuff():
	test = raw_input('Which code would you like to test? ')
	test = test.split(' ')
	rCode = test[0]
	data = test[1:]
	print 'Read: ',rCode,' ',data
	return rCode,data
	'''
	rec = linker.readLine()
	rCode = rec[0]
	data = rec[1:]
	return rCode,data
	'''

# Sends R-Code to links tx buffer		
def sendBuff(rCode,data):
	send = 'prime,'+rCode+'\n'+data+'\n'
	print send
	#linker.write(send)
	
# Based on state and R-Code recieved, send appropriate R-Code and information back			
def actOnRCode(rCode,data):	
	
	if state == 1:
		print 'State: 1'
		if rCode == 'R00': # Keep Alive
			print 'I got ' + rCode
		elif rCode == 'R01': # Kill
			print 'I got ' + rCode
		elif rCode == 'R02': # Power Down
			print 'I got ' + rCode
		elif rCode == 'R08': # State
			print 'I got ' + rCode
						
	if state == 2:
		print 'State: ',state
		if rCode == 'R00': # Keep Alive
			print 'I got ' + rCode
		elif rCode == 'R01': # Kill
			print 'I got ' + rCode
		elif rCode == 'R02': # Power Down
			print 'I got ' + rCode
		elif rCode == 'R05': # Enable Tele-op
			print 'I got ' + rCode
		elif rCode == 'R06': # Enable Autonomous
			print 'I got ' + rCode
		elif rCode == 'R07': # Mode (1=Auto 0=Tele)
			print 'I got ' + rCode
		elif rCode == 'R08': # State
			print 'I got ' + rCode
		elif rCode == 'R37': # Actual Twist
			print 'I got ' + rCode
		elif rCode == 'R50': # Gyro Rates
			print 'I got ' + rCode
			gyro = listener.gyro
			sendBuff(rCode,gyro)
		elif rCode == 'R51': # Acceleration
			print 'I got ' + rCode
			accel = listener.accel
			sendBuff(rCode,accel)
		elif rCode == 'R52': # Magnometer
			print 'I got ' + rCode
			magne = listner.magne
			sendBuff(rCode,magne)
		elif rCode == 'R53': # Heading
			print 'I got ' + rCode
	
	if state == 3:
		if rCode == 'R00': # Keep Alive
			pass
		elif rCode == 'R01': # Kill
			pass
		elif rCode == 'R02': # Power Down
			pass
		elif rCode == 'R05': # Enable Tele-op
			pass
		elif rCode == 'R06': # Enable Autonomous
			pass
		elif rCode == 'R07': # Mode (1=Auto 0=Tele)
			pass
		elif rCode == 'R08': # State
			pass
		elif rCode == 'R37': # Actual Twist
			pass
		elif rCode == 'R50': # Gyro Rates
			gyro = listener.gyro
			sendBuff(rCode,gyro)
		elif rCode == 'R51': # Acceleration
			accel = listener.accel
			sendBuff(rCode,ga)
		elif rCode == 'R52': # Magnometer
			gyro = listener.magne
			sendBuff(rCode,gyro)
		elif rCode == 'R53': # Heading
			pass
		elif rCode == 'R60': # Left Range
			pass
		elif rCode == 'R61': # Right Range
			pass
		elif rCode == 'R63': # Center Range
			pass
		elif rCode == 'R16': # Time since boot
			pass
					
	if state == 4:
		if rCode == 'R00': # Keep Alive
			pass
		elif rCode == 'R01': # Kill
			pass
		elif rCode == 'R02': # Power Down
			pass
		elif rCode == 'R05': # Enable Tele-op
			pass
		elif rCode == 'R06': # Enable Autonomous
			pass
		elif rCode == 'R07': # Mode (1=Auto 0=Tele)
			pass
		elif rCode == 'R08': # State
			pass
		elif rCode == 'R37': # Actual Twist
			pass
		elif rCode == 'R50': # Gyro Rates
			pass
		elif rCode == 'R51': # Acceleration
			pass
		elif rCode == 'R52': # Magnometer
			pass
		elif rCode == 'R53': # Heading
			pass
		elif rCode == 'R60': # Left Range
			pass
		elif rCode == 'R61': # Right Range
			pass
		elif rCode == 'R63': # Center Range
			pass
		elif rCode == 'R16': # Time since boot
			pass
		elif rCode == 'R20': # Add Waypoint
			pass
		elif rCode == 'R21': # Reset Waypoints
			pass
		elif rCode == 'R25': # Retrieve Waypoints
			pass
		elif rCode == 'R26': # Current Waypoint
			pass
		elif rCode == 'R27': # Next Waypoint
			pass
		elif rCode == 'R28': # Planned Route
			pass
		elif rCode == 'R40': # Position
			pass
		elif rCode == 'R41': # Accuracy
			pass
		elif rCode == 'R42': # Number of Satellites
			pass
						
	if state == 5:
		if rCode == 'R00': # Keep Alive
			pass
		elif rCode == 'R01': # Kill
			pass
		elif rCode == 'R02': # Power Down
			pass
		elif rCode == 'R05': # Enable Tele-op
			pass
		elif rCode == 'R06': # Enable Autonomous
			pass
		elif rCode == 'R07': # Mode (1=Auto 0=Tele)
			pass
		elif rCode == 'R08': # State
			pass
		elif rCode == 'R37': # Actual Twist
			pass
		elif rCode == 'R50': # Gyro Rates
			pass
		elif rCode == 'R51': # Acceleration
			pass
		elif rCode == 'R52': # Magnometer
			pass
		elif rCode == 'R53': # Heading
			pass	
		elif rCode == 'R60': # Left Range
			pass
		elif rCode == 'R61': # Right Range
			pass
		elif rCode == 'R63': # Center Range
			pass
		elif rCode == 'R16': # Time since boot
			pass	
		elif rCode == 'R20': # Add Waypoint
			pass
		elif rCode == 'R21': # Reset Waypoints
			pass
		elif rCode == 'R25': # Retrieve Waypoints
			pass
		elif rCode == 'R26': # Current Waypoint
			pass
		elif rCode == 'R27': # Next Waypoint
			pass
		elif rCode == 'R28': # Planned Route
			pass
		elif rCode == 'R40': # Position
			pass
		elif rCode == 'R41': # Accuracy
			pass
		elif rCode == 'R42': # Number of Satellites
			pass				
		elif rCode == 'R70': # Image Size
			pass
		elif rCode == 'R71': # JPEG Quality
			pass
		elif rCode == 'R75': # Fetch Image
			pass
		elif rCode == 'R76': # Fetch Depthmap
			pass
	

# And so it begins...
def main():

	while not rospy.is_shutdown():
		try:
			[rCode,data] = readBuff()
			print 'act'
			actOnRCode(rCode,data)
		except:		
			pass
			
main()
