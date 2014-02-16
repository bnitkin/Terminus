#!/usr/bin/python2
# Jan 2014
# Ben Nitkin
# 
# Base station frontend
# Sets up all widgets and talks to serial functions.  

#Library imports
import pygame, sys

#Local imports
import ui, rcode, link, buttons
from config import *

serialHandle = link.Serial()

def main():
	#Setup pygame	
	sys.stderr.write(">> Loading pygame.\n")
	pygame.init()
	clock = pygame.time.Clock() #Rate-limits framerate to 30fps.
	#Title and icon
	pygame.display.set_caption(TITLE)
	if sys.platform.startswith('darwin'): #OSX has a nice big canvas for drawing icons. Why not take advantage?
		pygame.display.set_icon(pygame.image.load(TITLE_ICON_MAC))
	else:
		pygame.display.set_icon(pygame.image.load(TITLE_ICON_WIN))

	window = pygame.display.set_mode((13*GRIDDING, int(8.5*GRIDDING)))
	window.fill(BACKGROUND)
	#Global variable sharing
	ui.Widget.window = window
	rcode.serial = serialHandle
	buttons.serial = serialHandle
	
	sys.stderr.write(">> Initializing joystick.\n")
	if pygame.joystick.get_count(): 
		pygame.joystick.Joystick(1)
	else: sys.stderr.write("!! Warning: no joystick found.\n")
	
	sys.stderr.write(">> Populating widgets.\n")
	#Setup buttons & layout

	#Camera & Map
	ui.Image('PS3 Eye', 4, 4, 640, 480)
	ui.Map('Map', 7*GRIDDING, 0, 6*GRIDDING, 5*GRIDDING)

	#Core gauges
	ui.Gauge('Speed  m/s', -3, 3, 1*GRIDDING, 5*GRIDDING)
	ui.Compass('Heading', 3*GRIDDING, 5*GRIDDING)
	ui.Gauge('Turn Rate', -3, 3, 5*GRIDDING, 5*GRIDDING)

	#Rangefinders
	ui.Light('Left', 1.5*GRIDDING, 7*GRIDDING) 
	ui.Light('Center', 3.5*GRIDDING, 7*GRIDDING)
	ui.Light('Right', 5.5*GRIDDING, 7*GRIDDING) 

	#Status lights
	ui.Light('Alive', 0*GRIDDING, 5*GRIDDING)
	ui.Light('Auto', 0*GRIDDING, 6*GRIDDING)

	#GPS stats
	ui.Text('Current Latitude', '00.00000N', 7*GRIDDING, 5*GRIDDING)
	ui.Text('Current Longitude', '00.00000W', 9*GRIDDING, 5*GRIDDING)
	ui.Text('Waypoint Latitude', '00.00000N', 7*GRIDDING, 6*GRIDDING)
	ui.Text('Waypoint Longitude', '00.00000W', 9*GRIDDING, 6*GRIDDING)
	ui.Text('Accuracy  m', '00.0', 11*GRIDDING, 5*GRIDDING)
	ui.Text('Satellites Tracked', '0', 11*GRIDDING, 6*GRIDDING)

	#Radio health
	ui.Text('Serial Framerate', '0', 7*GRIDDING, 7*GRIDDING)
	ui.Text('RX Rate  B/s', '0', 9*GRIDDING, 7*GRIDDING)

	#Buttons!
	ui.Button('E-Stop', buttons.kill, 0, 7.5*GRIDDING)
	ui.Button('Shutdown', buttons.poweroff, 0*GRIDDING, 8*GRIDDING)
	ui.Button('Teleop', buttons.teleautoswitch, 0*GRIDDING, 7*GRIDDING)	
	ui.Button('PrtScr', buttons.screenshot, 12*GRIDDING, 8*GRIDDING)
	ui.Button('Reset Map', buttons.mapreset, 11*GRIDDING, 8*GRIDDING)
	#Stats
	ui.Text('Uptime', '0', 11*GRIDDING, 7*GRIDDING)
	
	#Start Serial thread for grabbing and sending data and updating gauges
	sys.stderr.write(">> Opening serial communication.\n")
	serialHandle.start() #Start the serial monitor
	
	sys.stderr.write(">> Ready!\n")
	while True:
		#Redraw gauges every frame
		for gauge in ui.Widget.widgets.values():
			gauge.blit()
		
		#R-Code handling
		rcode.setGauges() #Flushes the serial buffer and sets gauges
		rcode.setState() #Sets robot state to enable/disable gauges
		
		#Event handling and callbacks
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				shutdown()
			if event.type == pygame.MOUSEBUTTONUP:
				for widget in ui.Widget.widgets.values():
					widget.mouseReleased()
			if event.type == pygame.MOUSEBUTTONDOWN:
				for widget in ui.Widget.widgets.values():
					widget.mousePressed()
			if event.type == pygame.MOUSEMOTION:
				for widget in ui.Widget.widgets.values():
					widget.mouseMoved()
			if event.type == pygame.JOYAXISMOTION:
				linear = joystick.get_axis(0) * MAX_VEL
				angular = joystick.get_axis(1) * MAX_TURN
				#Queue the current velocity for sending to the robot.
				serialHandle.write('R30 {:.3} {:.3}\n'.format(linear, angular))
			if event.type == pygame.JOYBUTTONDOWN: 
				pass
			if event.type == pygame.JOYBUTTONUP: 
				pass

		pygame.display.update()
		clock.tick(FRAMERATE)
		
def shutdown():
	sys.stderr.write(">> Shutting down.\n")
	sys.stderr.write(">> Requesting serial link shutdown.\n")
	serialHandle.stop()
	sys.stderr.write(">> Waiting for serial link to close.\n")
	serialHandle.join()
	sys.stderr.write(">> Exiting pygame.\n")
	pygame.quit()
	sys.stderr.write(">> Done.")
	sys.exit()

def run():
	try:
		main()
	except Exception, e:
		sys.stderr.write("!! Exception encountered. Shutting down.\n")
		sys.stderr.write("!! "+str(e)+'\n')
		shutdown()
	except KeyboardInterrupt, k:
		sys.stderr.write(">> Recieved Ctrl+C\n")
		shutdown()

if __name__ == '__main__': run()
