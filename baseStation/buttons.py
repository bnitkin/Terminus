#buttons.py
#Ben Nitkin
# Jan 2014
#
#Callback functions for buttons
#These functions manipulate individual buttons. 

import pygame
import ui
import time

def alive(widget):
	try:
		link.send('R00')
		widget.set(True)
	except:
		widget.set(False)
def kill(button):
	if button.name == 'E-Stop':
		link.send('R01')
		button.setname('Resume')
	else: 
		link.send('R00')
		button.setname('E-Stop')
		
def poweroff(button):
	if button.name != 'Confirm?': button.setname('Confirm?')
	else: link.send('R02')
	
def teleautoswitch(button):
	if button.name == 'Teleop':
		link.send('R05')
		button.setname('Autonav')
	if button.name == 'Autonav':
		link.send('R06')
		button.setname('Teleop')
		
def screenshot(button):
	pygame.image.save(ui.Widget.window, 'screenshots/{}.png'.format(int(time.time())))
