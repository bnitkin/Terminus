#!/usr/bin/python2
#Echoes any recieved transmissions.
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0)

while True:
	ser.write(ser.read())
