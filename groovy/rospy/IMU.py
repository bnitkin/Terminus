#Python Code to talk to the IMU
#Helen with Ben's help
#Goal: read data from the accelerometer and give it to ROS

#$-217,-153,18,255,4,-184,124,137,-2#

#A line of data from the IMU looks like the above line. 

import std_msgs.msg,geometry_msgs.msg
msg = sensor_msgs.msg.Imu()
