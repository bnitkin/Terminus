#!/usr/bin/env python
#Python Code to talk to the GPS
#Goal: read data from the GPS and give it to ROS
import serial,time,math,rospy,std_msgs.msg
from sensor_msgs.msg import NavSatFix,NavSatStatus

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)

#global ser
#ser = open('/home/optimus/Terminus/groovy/rospy/gps.txt', 'r')

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
    #SatUsed = float(GPSFixList[7])
    #Altitude
	Altitude = float(GPSFixList[9])
	print GPSFixList, '\n', Latitude, Longitude, Altitude, '\n'
	print 'Lat: ',Latitude,' Lon: ', Longitude,' Alt: ', Altitude
	return Latitude, Longitude, Altitude

def GPGLL(string):
	print 'and Geographic Position (Lat&Long)'
	return

def GPGSA(string):
	print 'and Active Satellites'
	return

def GPGSV(string):
	print 'and Satellites in view'
	return

def GPRMC(string):
	print 'and Recommended Minimum Specific Data'
	return

def GPVTG(string):
	print 'and Course Over Ground and Ground Speed'
	return



parsetype = {}
parsetype['$GPGGA'] = GPGGA #Global Positioning System Fix Data (time, position, #sat)
parsetype['$GPGLL'] = GPGLL #Geographic Position (Lat&Long)
parsetype['$GPGSA'] = GPGSA #Active Satellites
parsetype['$GPGSV'] = GPGLL #Satellites in view
parsetype['$GPRMC'] = GPRMC #Recommended Minimum Specific Data
parsetype['$GPVTG'] = GPVTG #Course Over Ground and Ground Speed




def parse():
	GPSraw = ser.readline()	#define the GPS raw data (from serial or sample)
	print GPSraw,'<- got it'
		#if GPSraw != '':
		#print GPSraw
	#if GPSraw[:6] in parsetype:
	if GPSraw[:6] == '$GPGGA':
		(lat,lon,alt) = GPGGA(GPSraw)
		#(lat,lon,alt) = parsetype[GPSraw[:6]](GPSraw)
		return lat,lon,alt
	else:
		print 'NOT GPGGA'

#Talker is to get it into ROS
def talker():
	print 'in talker'
	pub = rospy.Publisher('GPS', NavSatFix)
	rospy.init_node('talker')
	while not rospy.is_shutdown():
		#Assuming that parse will return these values
		try:
			(lat,lon,alt) = parse()
			print type(lat), type(lon), type(alt)
			
		except:
			continue
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

talker()
