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
import ui

laststate = ''

def set(name, value):
	"""Shorthand function for setting gauges."""
	ui.Widget.widgets[name].set(value)
	
def disable(name): 
	ui.Widget.widgets[name].disable()

def setState(serial):
	"""Transmits a robot set-state command based on incoming bandwidth."""
	#Set state
	state = 'R90' #The code to send to transition to state 5
	if serial.rxSpeed() < 10000: state = 'R40'
	if serial.rxSpeed() < 80: state = 'R30'
	if serial.rxSpeed() < 60: state = 'R20'
	if serial.rxSpeed() < 40: state = 'R10'
	if serial.rxSpeed() < 20: state = 'R00' #State 0 code (whatever that may be)
	
	if state == laststate: return
	serial.write(state)
	#Update gauges to reflect new state
	for widget in ui.Widget.widgets.values():
		widget.enable()

	if state == 'R90': return
	
	disable('PS3 Eye')
	if state == '4': return
	
	disable('Current Latitude')
	disable('Current Longitude')
	disable('Waypoint Latitude')
	disable('Waypoint Longitude')
	disable('Accuracy  m')
	disable('Satellites Tracked')
	disable('Uptime')
	if state == '3': return

	disable('Left')
	disable('Center')
	disable('Right')
	disable('Auto')
	if state == '2': return
		
	disable('Heading')
	disable('Turn Rate')
	disable('Speed  m/s')
	if state == '1': return

def setGauges(serial):
	"""Queries the serial buffer for codes and displays all recieved data."""
	#Set transmission rates every frame
	set('TX Rate  B/s', str(serial.txSpeed()))
	set('RX Rate  B/s', str(serial.rxSpeed()))
	
	while serial.hasCode():
		code, data = serial.readCode()
		#TODO: Decide on a protocol, then continue.
