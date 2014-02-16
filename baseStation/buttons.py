#buttons.py
#Ben Nitkin
# Jan 2014
#
#Callback functions for buttons
#These functions manipulate individual buttons. 

import pygame, time
import ui

serial = None

def alive(widget):
	try:
		serial.send('R00')
		widget.set(True)
	except:
		widget.set(False)
def kill(button):
	if button.name == 'E-Stop':
		serial.write('R01\n')
		button.setname('Resume')
	else: 
		serial.write('R00\n')
		button.setname('E-Stop')
		
def poweroff(button):
	if button.name != 'Confirm?': button.setname('Confirm?')
	else: serial.write('R02')
	
def teleautoswitch(button):
	if button.name == 'Teleop':
		serial.write('R05\n')
		button.setname('Autonav')
	if button.name == 'Autonav':
		serial.write('R06\n')
		button.setname('Teleop')
		
def screenshot(button):
	pygame.image.save(ui.Widget.window, 'screenshots/{}.png'.format(int(time.time())))

def mapreset(button):
	ui.Widget.widgets['Map'].cleartrack()
