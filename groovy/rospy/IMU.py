#!/usr/bin/env python
#Python Code to talk to the IMU
#Helen with Ben's help
#Goal: read data from the accelerometer and give it to ROS
import serial,math,rospy,std_msgs.msg
#ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1)

def parse():
 
    #raw = ser.readline()

    raw = "$11,22,33,44,55,66,77,88,99\r\n"

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
 #   print accel
    return (accel, gyro, magne)
    
def talker():
	pub = rospy.Publisher('chatter', std_msgs.msg.String)
	rospy.init_node('talker')
	while not rospy.is_shutdown():
        parse()
		pub.publish('polo')

talker()
