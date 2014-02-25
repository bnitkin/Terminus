#!/usr/bin/env python
#Python Code to talk to the GPS
#Goal: read data from the GPS and give it to ROS
import serial,math #rospy,std_msgs.msg
#ser = serial.Serial('/dev/tty.usbserial-A603AXN7', 9600, timeout=0.1)
ser = open('/Users/helen/Desktop/GPSDummyData.txt', 'r')

def GPGGA(GPSFixRaw):
    print 'We have fix data. Better learn to parse this... Let\'s try this...'
    GPSFixList = GPSFixRaw.strip('$GPGGA\n').split(',')
    Latitude =
    print GPSFixList
def gll(string):
    print 'and GLL'


parsetype = {}
parsetype['$GPGGA'] = GPGGA
parsetype['$GPGLL'] = gll





def parse():
    GPSraw = ser.readline()    #define the GPS raw data (from serial or sample)
        #if GPSraw != '':
        #print GPSraw
    if GPSraw[:6] in parsetype:
        parsetype[GPSraw[:6]](GPSraw)

"""
#Talker is to get it into ROS
def talker():
	
	pub = rospy.Publisher('chatter', std_msgs.msg.String)
	rospy.init_node('talker')
	while not rospy.is_shutdown():
		pub.publish('polo')
		        
    #import std_msgs.msg,geometry_msgs.msg
    #msg = sensor_msgs.msg.IMU()

def main():
    accel = []
    gyro = []
    magnet = []
    while True:
        try:
            accel, gyro, magnet =  parse()
            talker()           
        except: continue
        


main()
"""

while True: parse()

