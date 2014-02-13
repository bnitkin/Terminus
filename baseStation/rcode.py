#RCode.py
#Ben Nitkin
# Jan 2014
#
# RCode integration
# These functions glue gauges to the serial link. 
# They manage transmissions to and from serial (via link.Serial): 
#  Set state to limit transmissions based on bandwidth
#  Read all recieved data from link.Serial and set gauges as data arrives
#  Transmit joystick commands (button callbacks handle their own transmissions)
# Serial should be an active instance of link.Serial

#Import the dict of widgets, to set values
import ui, sys
from config import *
from pygame import time

laststate = 0

serclock = time.Clock()

codeIndex = {} #Mapping of string codes to functions.

def set(name, value):
	"""Shorthand function for setting gauges."""
	try:
		ui.Widget.widgets[name].set(value)
	except:
		sys.stderr.write("!! Could not set {} to {}.\n".fo)

def disable(name): 
	ui.Widget.widgets[name].disable()

def setState(serial):
	"""Transmits a robot set-state command based on incoming bandwidth."""
	#Set state based on the number of hits/s Alive gets.
	state = 5 #The code to send to transition to state 5
	if serclock.get_fps() < 12: state = 4
	if serclock.get_fps() < 10: state = 3
	if serclock.get_fps() < 8: state = 2
	if serclock.get_fps() < 2: state = 1
	
	serial.writeCode('R08 {}'.format(state)) #Retransmit state every 1/30 of a second.
	#Update gauges to reflect new state iff it's changed.
	global laststate

	if state == laststate: return
	laststate = state
	
	for widget in ui.Widget.widgets.values():
		widget.enable()

	if state == 5: return
	
	disable('PS3 Eye')
	if state == 4: return
	
	disable('Current Latitude')
	disable('Current Longitude')
	disable('Waypoint Latitude')
	disable('Waypoint Longitude')
	disable('Accuracy  m')
	disable('Satellites Tracked')
	disable('Map')
	if state == 3: return

	disable('Left')
	disable('Center')
	disable('Right')
	disable('Uptime')
	if state == 2: return
		
	disable('Heading')
	disable('Turn Rate')
	disable('Speed  m/s')
	disable('Auto')
	set('Alive', False) #We're in state 1 cause we can't talk to the robot.
	if state == 1: return

def setGauges(serial):
	"""Queries the serial buffer for codes and displays all recieved data."""
	#Set transmission rates every frame
	set('Serial Framerate', '{:.2f}'.format(serclock.get_fps()))
	set('RX Rate  B/s', str(serial.rxSpeed()))
	
	while serial.hasCode():
		code, data = serial.readCode()
		
		

def alive(data):
	serclock.tick() #Alive is the robot's pulse.
	set('Alive', True)

def auto(data):
	set('Auto', float(data))
	
def twist(data):
	speed, turn, blank = data.split('\n')
	set('Speed  m/s', float(speed))
	set('Turn Rate', float(turn))
	
def heading(data):
	set('Heading', float(data))
	
def lrange(data):
	dist = float(data)
	#Interpolate between MAX and MIN range; bound by 0..1
	color = min(max((dist - RANGE_MIN) / (RANGE_MAX - RANGE_MIN), 0), 1)
	set('Left', color)
	
def crange(data):	
	dist = float(data)
	#Interpolate between MAX and MIN range; bound by 0..1
	color = min(max((dist - RANGE_MIN) / (RANGE_MAX - RANGE_MIN), 0), 1)
	set('Center', color)
	
def rrange(data):	
	dist = float(data)
	#Interpolate between MAX and MIN range; bound by 0..1
	color = min(max((dist - RANGE_MIN) / (RANGE_MAX - RANGE_MIN), 0), 1)
	set('Right', color)
	
def uptime(data):
	set('Uptime', '{:.1f}'.format(float(data)))
	
def waypoint(data):
	slat, slon, blank = data.split('\n')
	lat, lon = float(slat), float(slon)
	#If lat/lon are positive, append N/E, else S/W.
	slat = '{: 10.5f}N'.format(lat) if lat>0 else '{: 10.5f}S'.format(lat)
	slon = '{: 10.5f}E'.format(lon) if lat>0 else '{: 10.5f}W'.format(lon)
	set('Waypoint Latitude', slat)
	set('Waypoint Longitude', slon)

def position(data):
	slat, slon, blank = data.split('\n')
	lat, lon = float(slat), float(slon)
	#If lat/lon are positive, append N/E, else S/W.
	slat = '{: 10.5f}N'.format(lat) if lat>0 else '{: 10.5f}S'.format(lat)
	slon = '{: 10.5f}E'.format(lon) if lat>0 else '{: 10.5f}W'.format(lon)
	set('Current Latitude', slat)
	set('Current Longitude', slon)
	set('Map', (lat, lon))
	
def accuracy(data):
	set('Accuracy  m', '{:.2f}'.format(float(data)))
	
def numsatellites(data):
	set('Satellites Tracked', int(data))
	
def image(data):
	set('PS3 Eye', data)

#State 1
codeIndex['R00'] = alive

#State 2
codeIndex['R07'] = auto
codeIndex['R37'] = twist
codeIndex['R53'] = heading

#State 3
codeIndex['R60'] = lrange
codeIndex['R61'] = crange
codeIndex['R62'] = rrange
codeIndex['R16'] = uptime

#State 4
codeIndex['R26'] = waypoint
codeIndex['R40'] = position
codeIndex['R41'] = accuracy
codeIndex['R42'] = numsatellites

#State 5
codeIndex['R70'] = image
