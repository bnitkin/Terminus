#Python Code to talk to the IMU
#Helen with Ben's help
#Goal: read data from the accelerometer and give it to ROS

import serial,math
ser = serial.Serial('/dev/tty.usbserial-A501VLXX', 57600, timeout=0.1)
raw = ser.readline()

#A line of data from the IMU looks like: 
stringsample = "$124,240,-102,-55,17,-11,-14,-265,47#"
IMUraw = raw	#define the IMU raw data (from serial or sample)
IMUraw = IMUraw.strip('$').strip('#\r\n')	#remove line marking characters
IMUlist = IMUraw.split(',')	#split into a list at commas
print raw,IMUlist

IMUlist = map(int,IMUlist)
accelraw = IMUlist[0:3]	#list 
gyroraw = IMUlist[3:6]
magneraw = IMUlist[6:9]


#Into metric
accel = map(lambda x:x*.0039*9.8,accelraw)	#m/s^2, check over many values
accelmag = (accel[1]**2+accel[2]**2+accel[0]**2)**.5

gyro = map(lambda x:x/14.375*3.14/180.0,gyroraw)	#radians per second
gyromag = (gyro[0]**2+gyro[1]**2+gyro[2]**2)**.5

magne = map(lambda x:x/(10000*230.0),magneraw)	#Tesla, needs reference to check
magnemag = (magne[0]**2+magne[1]**2+magne[2]**2)**.5

print 'Acceleration (m/s^2):',accel,'\t',accelmag
print 'Gyro (rad/s):',gyro,'\t',gyromag
print 'Magnetic Field (Tesla):',magne,'\t',magnemag

#import std_msgs.msg,geometry_msgs.msg
#msg = sensor_msgs.msg.IMU()
