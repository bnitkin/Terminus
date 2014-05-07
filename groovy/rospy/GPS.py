#!/usr/bin/env python
#Python Code to talk to the GPS
#Goal: read data from the GPS and give it to ROS
import serial,time,math,rospy,std_msgs.msg
from sensor_msgs.msg import NavSatFix,NavSatStatus

#ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=0.1)
ser = open('/home/optimus/Terminus/groovy/rospy/gps.txt', 'r')

class GPS():
	def __init__(self):
		self.lat = 0
		self.lon = 0
		self.alt = 0
		self.mode = 0
		self.head = 0
		self.numSat = 0
	
GPS = GPS()

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
    GPS.numSat = float(GPSFixList[7])
    #Altitude
	Altitude = float(GPSFixList[9])
	
	#Parsing Mode
	ModeRaw = GPSFixList[6]
	Mode = int(ModeRaw)
	
	print GPSFixList, '\n', Latitude, Longitude, Altitude, '\n'
	print 'Lat: ',Latitude,' Lon: ', Longitude,' Alt: ', Altitude
	return Latitude, Longitude, Altitude, Mode

def GPVTG(GPSFixRaw):
	GPSFixList = GPSFixRaw.strip('$GPVTG\n').split(',')
	print GPSFixList[1]
	head = float(GPSFixList[1])
	return head
	

def parse():
	GPSraw = ser.readline()	#define the GPS raw data (from serial or sample)
	print GPSraw,'<- got it'
		#if GPSraw != '':
		#print GPSraw
	#if GPSraw[:6] in parsetype:
	if GPSraw[:6] == '$GPGGA':
		(GPS.lat,GPS.lon,GPS.alt,GPS.mode) = GPGGA(GPSraw)
		#(lat,lon,alt) = parsetype[GPSraw[:6]](GPSraw)	
	#elif GPSraw[:6] == '$GPVTG':
	#	GPS.head = GPVTG(GPSraw)
	else:
		print 'NOT GPGGA or GPVTG'

#Talker is to get it into ROS
def talker():
	
	print 'in talker'
	pub = rospy.Publisher('GPS', NavSatFix)
	rospy.init_node('GPStalker')
	while not rospy.is_shutdown():
		#Assuming that parse will return these values
		time.sleep(1)
		parse()
		msg = NavSatFix()
		Fix = NavSatStatus()
		Fix.status = GPS.mode
		Fix.service = GPS.numSat
		
		msg.header.stamp = rospy.Time.now()
		msg.status = Fix
		msg.latitude = GPS.lat
		msg.longitude = GPS.lon
		msg.altitude = GPS.alt
		msg.position_covariance = (0, 0, 0, 0, 0, 0, 0, 0, 0)
		msg.position_covariance_type = 0
		#covariance_type = 0 unknown
		#                = 1 approximated
		#                = 2 diagonal known
		#                = 3 known
		pub.publish(msg)

def heading():
	publ = rospy.Publisher('GPS/Heading', float)
	rospy.init_node('heading')
	while not rospy.is_shutdown():
		msg = GPS.head
		publ.publish(msg)

talker()
#heading()
