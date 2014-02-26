#!/usr/bin/env python
#Python Code to talk to the GPS
#Goal: read data from the GPS and give it to ROS
import serial,math #,rospy,std_msgs.msg
#from sensor_msgs.msg import NavSatFix,NavSatStatus
#ser = serial.Serial('/dev/tty.usbserial-A603AXN7', 9600, timeout=0.1)
ser = open('/home/robot/Terminus/groovy/rospy/gps.txt', 'r')

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
	print GPSFixList, '\n',Latitude,Longitude
def GPGLL(string):
	print 'and GLL'

parsetype = {}
parsetype['$GPGGA'] = GPGGA
parsetype['$GPGLL'] = GPGLL





def parse():
	GPSraw = ser.readline()	#define the GPS raw data (from serial or sample)
		#if GPSraw != '':
		#print GPSraw
	if GPSraw[:6] in parsetype:
		parsetype[GPSraw[:6]](GPSraw)

"""
#Talker is to get it into ROS
def talker():
	
	pub = rospy.Publisher('GPS', NavSatFix)
	rospy.init_node('talker')
	while not rospy.is_shutdown():
		#Assuming that parse will return these values
		(lat,lon,alt) = parse()
		msg = NavSatFix()
		msg.header.stamp = rospy.Time.now()
		msg.latitude = lat
		msg.longitude = lon
		msg.altitude = alt
		msg.position_covariance = (0, 0, 0, 0, 0, 0, 0, 0, 0)
		msg.position_covariance_type = 0
		#covariance_type = 0 unknown
		#                = 1 approximated
		#                = 2 diagonal known
		#                = 3 known
		pub.publish(msg)
				
	#import std_msgs.msg,geometry_msgs.msg
	#msg = sensor_msgs.msg.IMU()
"""


while True: parse()

