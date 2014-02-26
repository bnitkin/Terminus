#!/usr/bin/env python
#Python Code to talk to the IMU
#Helen with Ben's help
#Goal: read data from the accelerometer and give it to ROS
import serial,math,rospy,std_msgs.msg
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3, Quaternion
#Uncomment line below when IMU is plugged in
#ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1)

def parse():
 
    #raw = ser.readline()

	#Use if IMU is not plugged in, but you want to test the code
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
	#Create publisher ('Topic name', msg type)
	pub = rospy.Publisher('IMU', Imu)
	#Tells rospy name of the node to allow communication to ROS master
	rospy.init_node('talker')

	while not rospy.is_shutdown():
		#Grab relevant information from parse()
		(accel,gyro,magne) = parse()
		
		#Define IMUmsg to be of the Imu msg type
		IMUmsg = Imu()
		
		#Set header time stamp
		IMUmsg.header.stamp = rospy.Time.now()
		
		#Set orientation parameters
		IMUmsg.orientation = Quaternion()
		IMUmsg.orientation.x = magne[0]
		IMUmsg.orientation.y = magne[1]
		IMUmsg.orientation.z = magne[2]
		IMUmsg.orientation_covariance = (0, 0, 0, 0, 0, 0, 0, 0, 0)
		
		#Set angular velocity parameters
		IMUmsg.angular_velocity = Vector3()
		IMUmsg.angular_velocity.x = gyro[0]
		IMUmsg.angular_velocity.y = gyro[1]
		IMUmsg.angular_velocity.z = gyro[2]
		IMUmsg.angular_velocity_covariance = (0, 0, 0, 0, 0, 0, 0, 0, 0)
		
		#Set linear acceleration parameters
		IMUmsg.linear_acceleration = Vector3()
		IMUmsg.linear_acceleration.x = accel[0]
		IMUmsg.linear_acceleration.y = accel[1]
		IMUmsg.linear_acceleration.z = accel[2]
		IMUmsg.linear_acceleration_covariance = (0, 0, 0, 0, 0, 0, 0, 0, 0)
		
		#Publish the data
		pub.publish(IMUmsg)

talker()
