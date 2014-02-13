#buttons.py
#Ben Nitkin
# Jan 2014
#
#Callback functions for buttons
#These functions manipulate individual buttons. 

import pygame, time
import ui, link

def alive(widget):
	try:
		link.send('R00')
		widget.set(True)
	except:
		widget.set(False)
def kill(button):
	if button.name == 'E-Stop':
		link.writeCode('R01')
		button.setname('Resume')
	else: 
		link.writeCode('R00')
		button.setname('E-Stop')
		
def poweroff(button):
	if button.name != 'Confirm?': button.setname('Confirm?')
	else: link.writeCode('R02')
	
def teleautoswitch(button):
	if button.name == 'Teleop':
		link.writeCode('R05')
		button.setname('Autonav')
	if button.name == 'Autonav':
		link.writeCode('R06')
		button.setname('Teleop')
		
def screenshot(button):
	pygame.image.save(ui.Widget.window, 'screenshots/{}.png'.format(int(time.time())))
