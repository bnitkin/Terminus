#Python Code to talk to the IMU
#Helen with Ben's help
#Goal: read data from the accelerometer and give it to ROS
import serial,math
ser = serial.Serial('/dev/tty.usbserial-A501VLXX', 57600, timeout=0.1)

def parse():
 #Change for where this is plugged in
    raw = ser.readline()

    IMUraw = raw	#define the IMU raw data (from serial or sample)
    IMUraw = IMUraw.strip('$#\r\n')	#remove line marking characters
    IMUlist = IMUraw.split(',')	#split into a list at commas

    IMUlist = map(int,IMUlist)
    accelraw = IMUlist[0:3]	#list
    gyroraw = IMUlist[3:6]
    magneraw = IMUlist[6:9]

    #Into metric
    accel = map(lambda x:x*.0039*9.8,accelraw)	#m/s^2, check over many values
    gyro = map(lambda x:x/14.375*3.14/180.0,gyroraw)	#radians per second
    magne = map(lambda x:x/(10000*230.0),magneraw)	#Tesla, needs reference to check
    return (accel, gyro, magne)

    #import std_msgs.msg,geometry_msgs.msg
    #msg = sensor_msgs.msg.IMU()

def main():
    accel = []
    gyro = []
    magnet = []
    while True:
        try:
            accel, gyro, magnet =  parse()
        except: continue


main()
