#!/usr/bin/env python2
#Autobot.py
#Prime's nemesis.
#Sources data from GPS, IMU, and Arduino; forwards everything to the
#base station via XBee.

#ROS was a great idea, but we're out of time. Here goes nothing.

#Attachment order: XBEE, GPS, IMU, Arduino. 
#This is important, since they enumerate in the order of plugging.
serXBEE    = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.1)
serGPS     = serial.Serial('/dev/ttyUSB1', 9600, timeout=0.1)
serIMU     = serial.Serial('/dev/ttyUSB2', 57600, timeout=0.1)
serArduino = serial.Serial('/dev/ttyUSB3', 9600, timeout=0.1)

def parseIMU():
 
    raw = serIMU.readline()

    IMUraw = raw	#define the IMU raw data (from serial or sample)
    IMUraw = IMUraw.strip('$#\r\n')	#remove line marking characters
    IMUlist = IMUraw.split(',')	#split into a list at commas

    IMUlist = map(int,IMUlist)
    accelraw = IMUlist[0:3]	#list
    gyroraw = IMUlist[3:6]
    magneraw = IMUlist[6:9]
    
    #testaccelraw = map(String,accelraw)

    #Into metric
    accel = map(lambda x:x*.0039*9.8,accelraw)	#m/s^2, check over many values
    gyro = map(lambda x:x/14.375*3.14/180.0,gyroraw)	#radians per second
    magne = map(lambda x:x/(10000*230.0),magneraw)	#Tesla, needs reference to check
    return (accel, gyro, magne)


def GPGGA(GPSFixRaw):
	print 'We have fix data. Better learn to parse this... Let\'s try this...'
	GPSFixList = GPSFixRaw.strip('$GPGGA\n').split(',')
	#Parsing Latitude
	LatitudeRaw = GPSFixList[2]
	LatitudeDegrees = int(LatitudeRaw[:2])
	LatitudeMinutes = float(LatitudeRaw[2:])
	if GPSFixList[3] == 'N':
		LatitudeDirection = 1
	if GPSFixList[3] == 'S':
		LatitudeDirection = -1
	Latitude = (LatitudeDegrees + LatitudeMinutes/60)*LatitudeDirection	#In decimal degrees
	
	#Parsing Longitude
	LongitudeRaw = GPSFixList[4]
	LongitudeDegrees = int(LongitudeRaw[:3])
	LongitudeMinutes = float(LongitudeRaw[3:])
	if GPSFixList[5] == 'E':
		LongitudeDirection = 1
	if GPSFixList[5] == 'W':
		LongitudeDirection = -1
	Longitude = (LongitudeDegrees + LongitudeMinutes/60)*LongitudeDirection
    #Satillites Used
    SatUsed = float(GPSFixList[7])
    #Altitude
	Altitude = float(GPSFixList[9])
	
	#Parsing Mode
	ModeRaw = GPSFixList[6]
	Mode = int(ModeRaw)
	
	print GPSFixList, '\n', Latitude, Longitude, Altitude, '\n'
	print 'Lat: ',Latitude,' Lon: ', Longitude,' Alt: ', Altitude
	return Latitude, Longitude, Altitude, Mode, SatUsed

def parseGPS():
	GPSraw = serGPS.readline()	#define the GPS raw data (from serial or sample)
	print GPSraw,'<- got it'
		#if GPSraw != '':
		#print GPSraw
	#if GPSraw[:6] in parsetype:
	if GPSraw[:6] == '$GPGGA':
		(lat,lon,alt,mode) = GPGGA(GPSraw)
		#(lat,lon,alt) = parsetype[GPSraw[:6]](GPSraw)
		return lat,lon,alt,mode
	else:
		print 'NOT GPGGA'

def parseArduino():
	Arduinoraw = serArduino.readline()	#define the GPS raw data (from serial or sample)
	return speed, (lrange, crange, rrange)
	
def main():
	accel = (0, 0, 0)
	gyro  =  (0, 0, 0)
	magne = (0, 0, 0)
	
	lat   = 0
	lon   = 0
	alt   = 0
	mode  = 0
	satnum = 0
	
	speed = 0
	rangefinders = (0, 0, 0)
	
	while True:
		#Grab data for each sensor, then burst it back to the base station.
		accel, gyro, magne = parseIMU()
		speed, rangefinders = parseArduino()
		try:
			lat, lon, alt, mode, satnum = parseGPS()
		except: 
			pass
		
			"""TO DO: define all of the send codes to return correct information"""
		
		heading = atan(magne[0]/magne[1])
		
		linker.write('prime,R00\n')	
		linker.write('prime,R07\n{}\n'.format(1)) #Tele-op or autonomous
		linker.write('prime,R37\n{}\n'.format(speed, 0)) 
		linker.write('prime,R53\n{}\n'.format(heading)) #Heading
		linker.write('prime,R60\n{}\n'.format(rangefinders[0])) #Need rangefinder info
		linker.write('prime,R61\n{}\n'.format(rangefinders[1])) #Need rangefinder info
		linker.write('prime,R62\n{}\n'.format(rangefinders[2])) #Need rangefinder info
		linker.write('prime,R16\n{}\n'.format(time.time()-start)) #Uptime
		linker.write('prime,R40\n{}\n{}\n'.format(lat, lon))   #position from GPS
		#linker.write('prime,R26 ', ['Need more', 'Need more'])   #current waypoint
		#linker.write('prime,R41 ', ['Not available'])      #accuracy of position
		linker.write('prime,R42\n{}\n'.format(satnum))  #Number of satellites
		#State 5
		#jpg = open('/home/optimus/Pictures/Webcam/2014-02-23-001737.jpg', 'r').read()
		#linker.write('prime,R70\n{}'.format(jpg))
		#if robot.state == 5: return
main()


##Working base station features: (15/23 things work; only 5 widgets are broken)
#Nope	ui.Image('PS3 Eye', 4, 4, 640, 480)
#Yep	ui.Map('Map', 7*GRIDDING, 0, 6*GRIDDING, 5*GRIDDING)

##Core gauges
#Yep	ui.Gauge('Speed  m/s', -3, 3, 1*GRIDDING, 5*GRIDDING)
#Yep	ui.Compass('Heading', 3*GRIDDING, 5*GRIDDING)
#Nope	ui.Gauge('Turn Rate', -3, 3, 5*GRIDDING, 5*GRIDDING)

##Rangefinders
#Yep	ui.Light('Left', 1.5*GRIDDING, 7*GRIDDING) 
#Yep	ui.Light('Center', 3.5*GRIDDING, 7*GRIDDING)
#Yep	ui.Light('Right', 5.5*GRIDDING, 7*GRIDDING) 

##Status lights
#Yep	ui.Light('Alive', 0*GRIDDING, 5*GRIDDING)
#Nope	ui.Light('Auto', 0*GRIDDING, 6*GRIDDING)

##GPS stats
#Yep	ui.Text('Current Latitude', '00.00000N', 7*GRIDDING, 5*GRIDDING)
#Yep	ui.Text('Current Longitude', '00.00000W', 9*GRIDDING, 5*GRIDDING)
#Nope	ui.Text('Waypoint Latitude', '00.00000N', 7*GRIDDING, 6*GRIDDING)
#Nope	ui.Text('Waypoint Longitude', '00.00000W', 9*GRIDDING, 6*GRIDDING)
#Sorta	ui.Text('Accuracy  m', '00.0', 11*GRIDDING, 5*GRIDDING)
#Yep	ui.Text('Satellites Tracked', '0', 11*GRIDDING, 6*GRIDDING)

##Radio health
#Yep	ui.Text('Serial Framerate', '0', 7*GRIDDING, 7*GRIDDING)
#Yep	ui.Text('RX Rate  B/s', '0', 9*GRIDDING, 7*GRIDDING)

##Buttons!
#Nope	ui.Button('E-Stop', buttons.kill, 0, 7.5*GRIDDING)
#Nope	ui.Button('Shutdown', buttons.poweroff, 0*GRIDDING, 8*GRIDDING)
#Nope	ui.Button('Teleop', buttons.teleautoswitch, 0*GRIDDING, 7*GRIDDING)     
#Yep	ui.Button('PrtScr', buttons.screenshot, 12*GRIDDING, 8*GRIDDING)
#Yep	ui.Button('Reset Map', buttons.mapreset, 11*GRIDDING, 8*GRIDDING)

##Stats
#Yep	ui.Text('Uptime', '0', 11*GRIDDING, 7*GRIDDING)
