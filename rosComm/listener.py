#!/usr/bin/env python
# Runs all ROS listeners for Base_to_ROS
# Derrick Hargwood
# February 2014
# Rev 1

import rospy
from sensor_msgs.msg import Imu,NavSatFix,NavSatStatus
from std_msgs.msg import Float64

class Quat():
	def __init__(self):
		self.x=0
		self.y=0
		self.z=0
		self.w=0
		
class listen():
	"""All ROS subscribers save their callback data in this class"""	
	def __init__(self):
		print 'init'
		#self.IMUlisten()
		self.LEFTlisten()
		#self.GPSlisten()
		self.head = 99
		self.left = 0
		self.center = 0
		self.right = 0
		self.lat = 147
		self.lon = 109	
		self.twist = 0.001
		self.numSat = 0
		self.accel = (0, 0, 0)
		self.gyro = (0, 0, 0)
		self.magne = Quat()
		# Need to pull odometry twist from ROS when autonomous is running
		
	# Callback function for IMUlisten
	def IMUinfo(self,data):
		self.accel = data.linear_acceleration
		self.gyro = data.angular_velocity
		self.magne = data.orientation
		
	# ROS subscriber to get IMU data
	def IMUlisten(self):
		rospy.init_node('IMUlisten', anonymous = True)
		rospy.Subscriber('IMU',Imu,self.IMUinfo)
		
	# Callback function for GPSlisten
	def GPSinfo(self,data):
		self.lat = data.latitude
		self.lon = data.longitude
		self.alt = data.altitude
		pok = data.status
		self.numSat = pok.service	

	# ROS subscriber to get GPS data
	def GPSlisten(self):
		rospy.init_node('GPSlisten', anonymous = True)
		rospy.Subscriber('GPS',NavSatFix,self.GPSinfo)
		
	# Callback function for left rangefinder data
	def LEFTinfo(self,data):
		self.left = data
	
	# ROS subscriber to get left range finder info
	def LEFTlisten(self):
		rospy.init_node('LEFTlisten', anonymous = True)
		rospy.Subscriber('LeftRange',Float64,self.LEFTinfo)
		
		
"""
	# Callback function for HEADlisten
	def HEADinfo(self,data):
		self.head = data

	# ROS subscriber to get heading data
	def HEADlisten(self):
		rospy.init_node('HEADlisten', anonymous = True)
		rospy.Subscriber('GPS/Heading',float,self.HEADinfo)
		rospy.spin()

	def JPGinfo(self,data)
		#Need to check data type
		self.img = data.data

	#ROS subscriber to get Images
	def JPGlisten(self)
		rospy.init_node('JPGlisten', anonymous = True)
		#Need to add correct topic name and msg type
		rospy.subscriber('/cameras/...',MSGTYPE,self.JPGinfo)
		#Also, spin might not be necessary more than once
		rospy.spin()
"""

