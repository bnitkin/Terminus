#!/usr/bin/python2
# Simple little script to create a dumb ROS slave node. It pings back 
# data using the right protocol but ignores serial buffering, real numbers, etc
import serial, time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0)
data = open('dummydata', 'r')
start = time.time()
state = 4

def sendcode(code, data=False):
	
	#Sends a nicely formatted code out with optional data.
	ser.write('prime,'+code+'\n')
	print 'prime,'+code+'\n',
	if data:
		for line in data:
			ser.write(str(line)+'\n')
			print str(line)+'\n',
def tx():
	print 'State', state
	#State 1
	sendcode('R00')
	if state == 1: return
	#State 2
	sendcode('R07', ['1'])
	sendcode('R37', [(time.time()/10)%6-3, (time.time()/10)%6-3])
	sendcode('R53', [time.time()*10%360])
	if state == 2: return

	#State 3
	sendcode('R60', [(time.time()/3)%5])
	sendcode('R61', [(time.time()/4)%6])
	sendcode('R62', [(time.time()/5)%7])
	sendcode('R16', [time.time()-start])
	if state == 3: return

	#State 4
	coord = data.readline().split(' ')
	sendcode('R40', [coord[1], coord[2]])
	sendcode('R26', [coord[1], coord[2]])
	sendcode('R41', [time.time()/2%8])
	sendcode('R42', [int(time.time())%30])
	if state == 4: return
	
	return #Suppress image for now.
	#State 5
	jpg = open('/home/ben/Downloads/7BD201B2-4950-4EA4-BE49-DD7007C6B51E.jpg', 'r').read()
	print jpg
	sendcode('R70', [jpg])
	if state == 5: return

def rx():
	while True:
		line = ser.readline()
		print line
		if line == '': return
		args = line.split(' ')
		code = args[0]
		
		if code == 'R08':
			global state
			try: state = int(args[1])
			except: print "Incomplete transmission:",args
		if code == 'R34': pass #This sets Twist
while True:
	tx()
	rx()
#	time.sleep(0.1)

