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
import ui, sys, re
from config import *
from pygame import time

laststate = 0
serclock = time.Clock()
codeIndex = {} #Mapping of string codes to functions.
flag = re.compile('ime,(R[0-9][0-9])$') #Allow for a missed newline and a few missed characters.

def set(name, value):
	"""Shorthand function for setting gauges."""
	ui.Widget.widgets[name].set(value)

def disable(name): 
	ui.Widget.widgets[name].disable()

def setState():
	"""Transmits a robot set-state command based on incoming bandwidth."""
	#Set state based on the number of hits/s Alive gets.
	state = 5 #The code to send to transition to state 5
	if serclock.get_fps() < 12: state = 4
	if serclock.get_fps() < 10: state = 3
	if serclock.get_fps() < 8: state = 2
	if serclock.get_fps() < 2: state = 1
	
	serial.write('R08 {}\n'.format(state)) #Retransmit state every 1/30 of a second.
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

def setGauges():
	"""Queries the serial buffer for codes and displays all recieved data."""
	#Set transmission rates every frame
	set('Serial Framerate', '{:.2f}'.format(serclock.get_fps()))
	set('RX Rate  B/s', str(serial.rxSpeed()))
	
	#If the buffer's less than 5 lines long, we have as much data as there is to grab.
	while serial.inWaiting() > 5:
		#Iterate until we hit a flag line.
		match = flag.search(serial.readLine())
		#Fire up code parsing.
		if match: 
			if codeIndex.has_key(match.group(1)): 
				try: codeIndex[match.group(1)]()
				except Exception, e: sys.stderr.write('!! {} on {}\n'.format(e, match.group(1)))
			else: 
				sys.stderr.write("!! Unknown code {}\n".format(match.group(1)))

		
def alive():
	serclock.tick() #Alive is the robot's pulse.
	set('Alive', True)

def auto():
	set('Auto', pullfloat(-.1, 1.1))
	
def twist():
	speed, turn = pulltwofloat((-5, 5), (-5, 5))
	set('Speed  m/s', float(speed))
	set('Turn Rate', float(turn))
	
def heading():
	set('Heading', pullfloat(0, 360))
	
def lrange():
	dist = pullfloat(-.1, 30)
	#Interpolate between MAX and MIN range; bound by 0..1
	color = min(max((dist - RANGE_MIN) / (RANGE_MAX - RANGE_MIN), 0), 1)
	set('Left', color)
	
def crange():	
	dist = pullfloat(-.1, 30)
	#Interpolate between MAX and MIN range; bound by 0..1
	color = min(max((dist - RANGE_MIN) / (RANGE_MAX - RANGE_MIN), 0), 1)
	set('Center', color)
	
def rrange():	
	dist = pullfloat(-.1, 30)
	#Interpolate between MAX and MIN range; bound by 0..1
	color = min(max((dist - RANGE_MIN) / (RANGE_MAX - RANGE_MIN), 0), 1)
	set('Right', color)
	
def uptime():
	set('Uptime', '{:.1f}'.format(pullfloat(0, 1E5)))
	
def waypoint():
	lat, lon = pulltwofloat((-180, 180), (-180, 180))
	#If lat/lon are positive, append N/E, else S/W.
	slat = '{: 10.5f}N'.format(lat) if lat>0 else '{: 10.5f}S'.format(lat)
	slon = '{: 10.5f}E'.format(lon) if lat>0 else '{: 10.5f}W'.format(lon)
	set('Waypoint Latitude', slat)
	set('Waypoint Longitude', slon)

def position():
	lat, lon = pulltwofloat((-180, 180), (-180, 180))
	#If lat/lon are positive, append N/E, else S/W.
	slat = '{: 10.5f}N'.format(lat) if lat>0 else '{: 10.5f}S'.format(lat)
	slon = '{: 10.5f}E'.format(lon) if lat>0 else '{: 10.5f}W'.format(lon)
	set('Current Latitude', slat)
	set('Current Longitude', slon)
	if len(ui.Widget.widgets['Map'].track) == 0:
		set('Map', (lat, lon))
	else:
		lastPos = ui.Widget.widgets['Map'].track[-1]
		dlat = abs(lat - lastPos[0])
		dlon = abs(lon - lastPos[1])
		if (dlat < MAX_MOVE/111130.0 and dlon < MAX_MOVE/111130.0):
			set('Map', (lat, lon))
	
def accuracy():
	acc = pullfloat(0, 200)
	set('Accuracy  m', '{:.2f}'.format(acc))
	
def numsatellites():
	set('Satellites Tracked', pullfloat(-.1,30))
	
def image():
	return
	set('PS3 Eye')

def pullfloat(floatrange, high = False):
	#Floatrange can be used as a low bound.
	if high: floatrange = (floatrange, high)
	"""Grabs data from the link buffer with plenty of error checking.
	floatrange is the allowed range of values for the incoming data."""
	#the main function pulls lines from the cache. This reads data in-place.
	l1 = serial.previewLine(0)
	value = 0
	try:
		value = float(l1)
	except:
		try: #Try to parse a float with at least 2 points after the decimal
			value = float(re.search('^[0-9]*\.[0-9]{2,}', l1).group(0))
		except: 
			raise ValueError('Could not parse {} as a float'.format(l1))
	if value > min(floatrange) and value < max(floatrange): return value
	else: raise ValueError('{} is out of the allowed range ({},{})'.format(value, min(floatrange), max(floatrange)))
	
def pulltwofloat(f1range, f2range):
	"""Grabs two floats from the link buffer with plenty of error checking.
	f1range and f2range are the allowed ranges of values for the incoming data."""
	f1 = pullfloat(f1range)
	serial.readLine()
	f2 = pullfloat(f2range)
	return f1, f2
	
def pullint():
	pass
	
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
