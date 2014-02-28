#!/usr/bin/env python
# Runs all ROS listeners for Base_to_ROS
# Derrick Hargwood
# February 2014
# Rev 1

import rospy
from sensor_msgs.msg import Imu,NavSatFix,NavSatStatus

class listen():
	"""All ROS subscribers save their callback data in this class"""	
	def __init__(self):
		print 'init'
		self.IMUlisten()
		#self.GPSlisten()
	
	# Callback function for IMUlisten
	def IMUinfo(self,data):
		self.accel = data.linear_acceleration
		self.gryo = data.angular_velocity
		self.magne = data.orientation		
					
	# ROS subscriber to get IMU data
	def IMUlisten(self):
		rospy.init_node('IMUlisten', anonymous = True)
		rospy.Subscriber('IMU',Imu,self.IMUinfo)
		print 'no-spin'
'''
	# Callback function for GPSlisten
	def GPSinfo(self,data):
		self.lat = data.latitude
		self.lon = data.longitude
		self.alt = data.altitude	

	# ROS subscriber to get GPS data
	def GPSlisten(self):
		rospy.init_node('GPSlisten', anonymous = True)
		rospy.Subscriber('GPS',NavSatFix,self.GPSinfo)
		rospy.spin()
'''
