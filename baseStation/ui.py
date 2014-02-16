#!/usr/bin/python2
# Jan 2014
# Ben Nitkin
# 
# UI functions for the base station. 
# Includes class definitions for buttons and gauges

import pygame, math, tempfile

from config import *

pygame.font.init()
title = pygame.font.Font(TITLE_NAME, TITLE_SIZE)
label = pygame.font.Font(LABEL_NAME, LABEL_SIZE)
digital = pygame.font.Font(DIGITAL_NAME, DIGITAL_SIZE)

def format(number, leading = 0, places=1):
	s= '{:0'+str(leading+places)+'.'+str(places)+'f}'
	return s.format(number)
	
def linepopulate(surface, anglestart, anglerange, numlines, linelength, annotation = {}):
	for l in range(numlines+1):
		angle = anglestart + anglerange*l/numlines
		start = (WIDGET_WIDTH/2 + (WIDGET_RADIUS-TICK_LENGTH)*math.sin(-angle), 
			WIDGET_HEIGHT/2 + (WIDGET_RADIUS-TICK_LENGTH)*math.cos(angle)) 
		end = (WIDGET_WIDTH/2 + WIDGET_RADIUS*math.sin(-angle), 
			WIDGET_HEIGHT/2 + WIDGET_RADIUS*math.cos(angle)) 
		pygame.draw.line(surface, TICK_COLOR, start, end, BORDER_THICKNESS)
		if annotation.has_key(l):
			text = label.render(str(annotation[l]), True, FONT_COLOR)
			dest = (WIDGET_WIDTH/2 - text.get_width()/2 + (WIDGET_RADIUS-LABEL_INSET)*math.sin(-angle), 
			WIDGET_HEIGHT/2 - text.get_height()/2+ (WIDGET_RADIUS-LABEL_INSET)*math.cos(angle)) 
			pygame.Surface.blit(surface, text, dest)

class Widget(pygame.Surface):
	"""A widget is a thing that goes on screen to display data. The core widget class
	provides for positioning and creates self.surface for subclasses to draw on with the draw()
	function. blit() redraws the widget on the main screen."""
	window = None
	widgets = {}
	error = None
	def __init__(self, name='Widget', x=0, y=0, width=WIDGET_WIDTH, height=WIDGET_HEIGHT):
		pygame.Surface.__init__(self, (width, height))
		self.name = name
		self.pressed = False
		self.hover = False
		self.x = x
		self.y = y
		self.clean = False
		self.active = True
		self.warn = False
		self.error = Error()
		self.timeoff = 0
		Widget.widgets[self.name] = self #Keep a list of all Widgets.
		
	def blit(self):
		"""Blit the widget to the master canvas window'"""
		if not self.clean: 
			self.draw() #Redraw the Surface if anything's changed.
			#If widget is inactive, push an error up. Remove it when activity resumes.
			if self.warn:
				self.error.blit(self, (self.get_width()/2-self.error.get_width()/2, self.get_height()/2-self.error.get_height()/2))
			clean = True
			try:
				self.window.blit(self, (self.x, self.y))
			except:
				raise Exception("Define Widget.window as the main PyGame canvas before blitting.")
	
	#The enable flag controls data update and is toggled to maintain framerate.
	def disable(self): 
		self.active = False
		self.error.settitle('Disabled')
		self.error.setmessage('Low bandwidth')
		self.setwarn()
		self.clean = False
	def enable(self):  
		if self.error.title == 'Disabled': self.clearwarn()
		self.active = True
		self.clean = False
	#The warn flag controls visibility of self.Error()
	def setwarn(self):
		self.warn = True
		self.clean = False
	def clearwarn(self):
		self.warn = False
		self.clean = False
	
	def remove(self):
		"""Remove the widget from the canvas"""
		Widget.widgets.remove(self)
		
	def draw(self):
		pass
		
	def mousePressed(self):
		if self.get_rect(top=self.y, left=self.x).collidepoint(pygame.mouse.get_pos()):
			self.pressed = True
			self.clean = False
	def mouseReleased(self):
		if self.pressed: 
			self.mouseClicked()
			self.pressed = False
			self.clean = False
	def mouseMoved(self):
		if self.get_rect(top=self.y, left=self.x).collidepoint(pygame.mouse.get_pos()):
			self.hover = True
			self.clean = False
		elif self.hover == True:
			self.hover = False
			self.clean = False
	def mouseClicked(self):
		"""This function fires on a mouse press followed by release."""
		pass

class Error(pygame.Surface):
	"""An error message that vanishes when clicked."""
	def __init__(self, name='Error', message='No Data', width=0.66*WIDGET_WIDTH, height=0.33*WIDGET_HEIGHT):
		pygame.Surface.__init__(self, (width, height))
		self.title = name
		self.message = message
		self.draw()
		
	def blit(self, dest, coord):
		if not self.clean: self.draw()
		pygame.Surface.blit(dest, self, coord)
	
	def setmessage(self, message): 
		self.message = message
		self.clean = False
		
	def settitle(self, title): 
		self.title = title
		self.clean = False
	
	def draw(self):
		self.clean = True
		pygame.draw.rect(self, WARN_FILL, (0, 0, self.get_width(), self.get_height()))
		pygame.draw.rect(self, WARN_BORDER, (0, 0, self.get_width(), self.get_height()), BORDER_THICKNESS)
		name = title.render(self.title, True, WHITE)
		pygame.Surface.blit(self, name, (self.get_width()/2-name.get_width()/2, BORDER_THICKNESS*3))
		sub = label.render(self.message, True, WHITE)
		pygame.Surface.blit(self, sub, (self.get_width()/2-sub.get_width()/2, self.get_height()-2*sub.get_height()))

class Image(Widget):
	"""Defines an image."""
	def __init__(self, name='Image', x=0, y=0, width=640, height=480):
		Widget.__init__(self, name, x, y, width, height)
		self.data = pygame.Surface((640, 480))
		novideo = title.render('No Video', True, WHITE)
		pygame.Surface.blit(self.data, novideo, (self.get_width()-novideo.get_width()-20, 20))

	def set(self, image):
		"""Uses PyGame to load images into a frame. 
		image should be a raw bitstream."""
		#Pygame can't deal with jpeg as a bitstream, so save a tempfile, then read it.
		self.clean = False
		img = tempfile.TemporaryFile()
		img.write(image)
		img.seek(0)
		self.data = pygame.image.load(img)
	def draw(self):
		self.clean = True
		#Blit image, centered on Image surface.	
		self.fill(BACKGROUND)
		pygame.Surface.blit(self, self.data, ((self.get_width()-self.data.get_width())/2, (self.get_height()-self.data.get_height())/2))
		pygame.draw.rect(self, MAP_BORDER, (0, 0, self.get_width(), self.get_height()), BORDER_THICKNESS)

class Button(Widget):
	def __init__(self, name='Button', callback = None, x=0, y=0):
		Widget.__init__(self, name, x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
		self.callback = callback
		self.clicked = False
		
	#Buttons can't be disabled
	def disable(self):
		return
	def enable(self):
		return
	def setwarn(self):
		pass
	def clearwarn(self):
		pass
	def setname(self, name):
		self.name = name
		self.clean = False
	def mouseClicked(self):
		"""Implements a callback for the button."""
		#Fire callback.
		self.callback(self)
		
	def draw(self):
		"""Draws the button on the default canvas"""
		self.clean = True
		self.fill(BACKGROUND)
		fill = BUTTON_NORMAL
		topleft = BUTTON_BORDER_2
		bottomright = BUTTON_BORDER_1
		textoffset = 0
		if self.hover: fill = BUTTON_HOVER
		if self.pressed: 
			fill = BUTTON_PRESS
			topleft = BUTTON_BORDER_1
			bottomright = BUTTON_BORDER_2
			textoffset = BORDER_THICKNESS/2
		rect = (BUTTON_MARGIN, BUTTON_MARGIN, self.get_width()-BUTTON_MARGIN*2, self.get_height()-BUTTON_MARGIN*2)
		pygame.draw.rect(self, fill, (BUTTON_MARGIN, BUTTON_MARGIN, self.get_width()-BUTTON_MARGIN*2, self.get_height()-BUTTON_MARGIN*2))
		#Shade bottom/right
		pygame.draw.rect(self, bottomright, ((rect[0], rect[1]), (rect[2], rect[3])), BORDER_THICKNESS)
		#Shade top/left
		pygame.draw.lines(self, topleft, False, ((rect[0], rect[3]), (rect[0], rect[1]), (rect[2], rect[1])), BORDER_THICKNESS)
		name = title.render(self.name, True, BLACK)
		pygame.Surface.blit(self, name, (textoffset + self.get_width()/2-name.get_width()/2, textoffset + self.get_height()/2-name.get_height()/2))
		
class StatusWidget(Widget):
	"""Defines a speedometer-style gauge"""
	def __init__(self, name='Gauge', minimum=0, maximum=100, x=0, y=0, scalestart = SCALE_START, scalerange = SCALE_RANGE):
		Widget.__init__(self, name, x, y)
		self.minimum = minimum
		self.maximum = maximum
		self.range = self.maximum-self.minimum
		self.scalestart = scalestart
		self.scalerange = scalerange
		self.value = 42
		self.set(0)  #Starting value
		self.leading = 2
		self.decimal = 2 		
		
	def set(self, value):
		"""Sets the gauge to a value"""
		if self.warn: self.clearwarn()
		self.clean = False
		self.value = value
		#Value normalized in the range of 0...1
		self.normalized = float(self.value-self.minimum)/self.range
		if self.normalized > 1.05: self.normalized = 1.05
		elif self.normalized < -0.05: self.normalized = -0.05
			
	def get(self): 
		return self.value
	
	def draw(self):
		"""Draws the widget"""
		self.clean = True
		self.fill(BACKGROUND)
		#Gauge background
		pygame.draw.circle(self, DIAL_FILL, (WIDGET_WIDTH/2, WIDGET_HEIGHT/2), WIDGET_RADIUS)
		circle(self, DIAL_BORDER, (WIDGET_WIDTH/2, WIDGET_HEIGHT/2), WIDGET_RADIUS, BORDER_THICKNESS)
		#Text
		text = digital.render(format(self.value, self.leading, self.decimal), True, DIGITAL_COLOR)
		dest = (WIDGET_WIDTH/2-text.get_width()/2,	WIDGET_HEIGHT - DIGITAL_FROM_BOTTOM)
		pygame.Surface.blit(self, text, dest)
		
		text = title.render(self.name, True, FONT_COLOR)
		dest = (WIDGET_WIDTH/2-text.get_width()/2,	WIDGET_HEIGHT - TITLE_FROM_BOTTOM)
		pygame.Surface.blit(self, text, dest)
		
		#Needle
		angle = self.scalerange * self.normalized + self.scalestart
		shape = ((WIDGET_WIDTH/2 + NEEDLE_RADIUS*math.sin(-angle), WIDGET_HEIGHT/2 + NEEDLE_RADIUS*math.cos(angle)), 
			(WIDGET_WIDTH/2 + 5*math.sin(-angle-math.pi*0.5), WIDGET_HEIGHT/2 + 5*math.cos(angle+math.pi*0.5)), 
			(WIDGET_WIDTH/2 + 5*math.sin(-angle-math.pi*1.5), WIDGET_HEIGHT/2 + 5*math.cos(angle+math.pi*1.5)))
		pygame.draw.polygon(self, NEEDLE_FILL, shape)
		pygame.draw.lines(self, NEEDLE_BORDER, True, shape, BORDER_THICKNESS/2)
		
class Gauge(StatusWidget):
	"""Defines a speedometer-style gauge"""
	def draw(self):
		"""Draws the widget"""
		StatusWidget.draw(self)	
		
		#Lines
		values = {0:format(self.minimum), TICKS/2: format(self.minimum+float(self.range)/2), TICKS:format(self.maximum)}
		linepopulate(self, self.scalestart, self.scalerange, TICKS, TICK_LENGTH, values)
		
		#Center thingey
		centerfill = pygame.Color(0, 0, 0, 0)
		hue = self.normalized * (CENTER_HUE_DANGER - CENTER_HUE_NORMAL) + CENTER_HUE_NORMAL
		if hue <   0: hue += 360
		if hue > 360: hue -= 360
		centerfill.hsva = (hue, CENTER_SAT, CENTER_VAL, 100)
		pygame.draw.circle(self, centerfill, (WIDGET_WIDTH/2, WIDGET_HEIGHT/2), CENTER_RADIUS)
		circle(self, CENTER_BORDER, (WIDGET_WIDTH/2, WIDGET_HEIGHT/2), CENTER_RADIUS, BORDER_THICKNESS)

class Compass(StatusWidget):
	def __init__(self, name='Compass', x=0, y=0):
		StatusWidget.__init__(self, name, 0, 360, x, y, 0, 2*math.pi)
		self.leading = 3
		self.decimal = 0
	def set(self, value):
		"""Sets the gauge to a value"""
		if self.warn: self.clearwarn()
		self.clean = False
		self.value = value%360
		self.normalized = float(self.value-self.minimum)/self.range+0.5
		if self.normalized > 1: self.normalized -= 1					
	
	def draw(self):
		StatusWidget.draw(self)
		directions = {1:'West', 2:'North', 3:'East'}
		linepopulate(self, 0, 2*math.pi, 4, TICK_LENGTH*2, directions)
		directions = {1:'SW', 3:'NW', 5:'NE', 7:'SE'}
		linepopulate(self, self.scalestart, self.scalerange, TICKS, TICK_LENGTH, directions)
	
class Progressbar(StatusWidget):
	"""Defines a progressbar type gauge"""
	def draw(self):
		"""Draws the progressbar"""
		pass

class Text(Widget):
	def __init__(self, name='TextBox', content='88888', x=0, y=0, width=TEXTBOX_WIDTH, height=TEXTBOX_HEIGHT):
		Widget.__init__(self, name, x, y, width, height)
		self.content = content
		self.lalign = False #Whether to left- or right-align
		
	def set(self, content):
		if self.warn: self.clearwarn()
		try: 
			self.content = '{:4.2f}'.format(content)
		except: 
			self.content = str(content)
		self.clean = False
		
	def draw(self):
		self.clean = True
		self.fill(BACKGROUND)
		rect = (TEXTBOX_TEXT_BORDER, self.get_height()-TEXTBOX_TEXT_BORDER, self.get_width()-2*TEXTBOX_TEXT_BORDER, -TEXTBOX_TEXT_HEIGHT)
		pygame.draw.rect(self, TEXTBOX_FILL, rect)
		pygame.draw.rect(self, TEXTBOX_BORDER, rect, BORDER_THICKNESS)
		name = title.render(self.name, True, TEXTBOX_TITLE_COLOR)
		pygame.Surface.blit(self, name, (TEXTBOX_TEXT_BORDER, self.get_height() - TEXTBOX_TEXT_BORDER*2 - TEXTBOX_TEXT_HEIGHT-name.get_height()))
		sub = digital.render(self.content, True, DIGITAL_COLOR)
		if self.lalign: xcoord = TEXTBOX_TEXT_BORDER*2
		else: xcoord = self.get_width()-sub.get_width()-2*TEXTBOX_TEXT_BORDER
		pygame.Surface.blit(self, sub, (xcoord, (self.get_height()-TEXTBOX_TEXT_HEIGHT/2) - sub.get_height()/2-TEXTBOX_TEXT_BORDER))

class Light(Widget):
	def __init__(self, name='Indicator', x=0, y=0, width=WIDGET_WIDTH/2, height=WIDGET_HEIGHT/2):
		Widget.__init__(self, name, x, y, width, height)
		self.state = False #Init value to off.
		#self.error = Error(width=0.3*WIDGET_WIDTH, height=0.3*WIDGET_HEIGHT)

	def set(self, state):
		"""Sets the current state of the Light. Can be True, False, or a float in the 0...1 range."""
		if self.warn: self.clearwarn()
		self.state = state
		
	def draw(self):
		self.clean = True
		self.fill(BACKGROUND)
		centerfill = pygame.Color(0, 0, 0, 0)
		hue = self.state * (CENTER_HUE_NORMAL-CENTER_HUE_DANGER) + CENTER_HUE_DANGER
		if hue <   0: hue += 360
		if hue > 360: hue -= 360
		centerfill.hsva = (hue, CENTER_SAT, CENTER_VAL, 100)
		pygame.draw.circle(self, centerfill, (WIDGET_WIDTH/4, WIDGET_HEIGHT/4), LIGHT_RADIUS)
		circle(self, CENTER_BORDER, (WIDGET_WIDTH/4, WIDGET_HEIGHT/4), LIGHT_RADIUS, BORDER_THICKNESS)
		name = title.render(self.name, True, BLACK)
		pygame.Surface.blit(self, name, (self.get_width()/2-name.get_width()/2,self.get_height()/2-name.get_height()/2))

class Map(Widget):
	def __init__(self, name='Map', x=0, y=0, width=600, height=600):
		Widget.__init__(self, name, x, y, width, height)
		self.track = []
		self.points = []
		self.resize = True
		self.reset() #Set latitude and longitude to defaults. Forces a resize on next blit.
	
	def mouseClicked(self):
		#On mouseclicked, wipe 1/2 of the track and rescale.
		self.track = self.track[len(self.track)/2+1:]
		self.redraw()
	#The map reblits poorly if it's disabled, so the warning is suppressed.
	def disable(self):
		return
	def enable(self):
		return
	def setwarn(self):
		pass
	def clearwarn(self):
		pass
	def reset(self):
		self.minlon = 10000
		self.minlat = 10000
		self.maxlon = -10000
		self.maxlat = -10000
		self.clat = 10000
		self.clon = 10000
		self.dlat = 0
		self.dlon = 0
		
	def point(self, coord, color):
		"""Adds a point to the map. Waypoints, obstacles, etc, can all be represented as colored points."""
		if self.contains(coord): self.drawwaypoint((coord, color))
		self.points.append((coord, color))
		self.clean = False
		
	def set(self, coord):
		"""Adds a point to the robot's track. Format is (lat, lon) in decimal degrees. Negative for south/west, as per ROS spec"""
		if self.warn: self.clearwarn()
		if self.contains(coord) and len(self.track): self.drawtrackline(self.track[-1], coord)
		self.clean = False
		self.track.append(coord)
	
	def clear(self):
		self.cleartrack()
		self.clearpoints()
	
	def cleartrack(self):
		self.clean = False
		self.resize = True
		self.track = []
		self.reset()

	def clearpoints(self):
		self.clean = False
		self.points = []
		self.reset()
	
	def draw(self):
		self.clean = True
		if self.resize: self.redraw()
		if len(self.track): pos = '({: 10.5f}, {: 10.5f})'.format(self.track[-1][0], self.track[-1][1])
		else: pos = '(  0.00000,  0.00000)'
		current = label.render(pos, True, FONT_COLOR, MAP_FILL)
		pygame.Surface.blit(self, current, (self.get_width()-current.get_width()-MAP_MARGIN*2, self.get_height()-2*MAP_MARGIN-current.get_height()))
		
	def redraw(self):
		self.clean = True
		self.resize = False
		self.fill(BACKGROUND)
		self.fill(MAP_FILL, (MAP_MARGIN, MAP_MARGIN, self.get_width()-2*MAP_MARGIN, self.get_height()-2*MAP_MARGIN))
		pygame.draw.rect(self, MAP_BORDER, (MAP_MARGIN, MAP_MARGIN, self.get_width()-2*MAP_MARGIN, self.get_height()-2*MAP_MARGIN), BORDER_THICKNESS)
		
		#Find the max and min latitudes out of all plotted points.
		latmin, lonmin, latmax, lonmax = 10000, 10000, -10000, -10000
		for coord in self.track:
			if coord[0] > latmax: latmax = coord[0]
			if coord[0] < latmin: latmin = coord[0]
			if coord[1] > lonmax: lonmax = coord[1]
			if coord[1] < lonmin: lonmin = coord[1]
		for waypoint in self.points:
			if waypoint[0][0] > latmax: latmax = waypoint[0][0]
			if waypoint[0][0] < latmin: latmin = waypoint[0][0]
			if waypoint[0][1] > lonmax: lonmax = waypoint[0][1]
			if waypoint[0][1] < lonmin: lonmin = waypoint[0][1]
		
		
		latc = (latmax-latmin)*RESIZE_AREA+latmin
		lonc = (lonmax-lonmin)*RESIZE_AREA+lonmin
		latlonratio = math.cos(latc * 3.1415/180)
		latrange = max(2*(latmax-latmin), 10E-5) #Set a hard minimum of 10E-6 degrees, about 1 meter.
		lonrange = max(2*(lonmax-lonmin), 10E-5) #The minimum size for the canvas, including buffer area.
		if self.get_height() * latrange / latlonratio > self.get_width() * lonrange: #Enlarge longitude
			lonrange = 1.0*self.get_width()/self.get_height()  * latrange / latlonratio
		else: #Enlarge latitude
			latrange = 1.0*self.get_height()/self.get_width() * lonrange * latlonratio
		
		#Save generated coordinates.
		self.minlat = latc - latrange/2
		self.maxlat = latc + latrange/2
		self.minlon = lonc - lonrange/2
		self.maxlon = lonc + lonrange/2
		self.clat = latc
		self.clon = lonc
		self.dlat = latrange
		self.dlon = lonrange
		#Draw waypoints and tracklines
		for i in range(len(self.track)-1):
			self.drawtrackline(self.track[i], self.track[i+1])
		for waypoint in self.points:
			self.drawwaypoint(waypoint)
		#Draw scale 
		#1* N/S = 110.567 km at 0* N at the equator and 111.699 km at 90* N Avg 111.13km/(* N/S)
		scale = self.dlon*SCALE_SIZE*111130
		scale = round(scale, -int(math.log10(abs(scale))))
		scaletext = '{:.0f} m'.format(scale)
		if scale > 1000: scaletext = '{:.0f} km'.format(scale/1000)
		pygame.draw.line(self, SCALE_COLOR, (MAP_MARGIN*4, self.get_height()-4*MAP_MARGIN), (MAP_MARGIN*4+scale/111130/self.dlon * self.get_width(), self.get_height()-4*MAP_MARGIN), BORDER_THICKNESS)
		scalesurf = label.render(scaletext, True, FONT_COLOR)
		pygame.Surface.blit(self, scalesurf, (MAP_MARGIN*4, self.get_height()-4*MAP_MARGIN-scalesurf.get_height()))

	def drawwaypoint(self, waypoint):
		pygame.draw.circle(self, waypoint[1], self.conv(waypoint[0]), FEATURE_SIZE)

	def drawtrackline(self, point1, point2):
		pygame.draw.aaline(self, TRACK_COLOR, self.conv(point1), self.conv(point2), 1)
	
	def contains(self, coord):
		"""Tests if the map needs to be redrawn and takes action, if so."""		
		#Create a bounding box that excludes the 10% nearest the edge of the map.
		maxlon, minlon = self.clon + MAX_AREA/2.0*self.dlon, self.clon - MAX_AREA/2.0*self.dlon	
		maxlat, minlat = self.clat + MAX_AREA/2.0*self.dlat, self.clat - MAX_AREA/2.0*self.dlat
		
		#Return True if the point is out of the bounding box.
		if (maxlon < coord[1]) or (minlon > coord[1]) or (maxlat < coord[0]) or (minlat > coord[0]): 
			self.resize = True
			return False
		return True
		
	def conv(self, coord):
		"""Converts an input lat/lon pair to an output pixel pair. Uses rectangular coordinates."""
		#Aliases for readability
		lat = coord[0]
		lon = coord[1]
		
		y = int(self.get_height() - (lat-self.minlat)/(self.maxlat - self.minlat) * self.get_height()) #To make math simpler, this doesn't filter down to just the map canvas.
		x = int((lon-self.minlon)/(self.maxlon - self.minlon) * self.get_width())
		return (x, y)


def circle(surface, color, pos, radius, width):
	"""Pygame's default border circle is awful - pixels leak 
	through from the background, so I wrote my own."""
	points = max(15, radius/2) #How many points to use.
	pointlist = []
	for x in range(points):
		pointlist.append((
			pos[0] + radius*math.sin(2*math.pi*x/points), 
			pos[1] + radius*math.cos(2*math.pi*x/points)))
	pygame.draw.lines(surface, color, True, pointlist, width)

if __name__ == '__main__':
	pygame.init()
	clock = pygame.time.Clock() #Rate-limits framerate to 30fps.
	window = pygame.display.set_mode((7*GRIDDING, 6*GRIDDING))
	window.fill(BACKGROUND)
	f = open('res/dummygpsdata')
	m = Map('Map', 0 , 0, 6*GRIDDING, 5*GRIDDING)
	Widget.window = window
	
	while True:
		#Redraw gauges every frame
		d = f.readline().split('"')
		if len(d) > 3 : m.set((float(d[1]), float(d[3])))
		else: 
			f.seek(0)
			m.redraw()
			m.cleartrack()
		for gauge in Widget.widgets.values():
			gauge.blit()
		pygame.display.update()
		clock.tick(FRAMERATE*2)

		#Event handling and callbacks
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				shutdown()
			if event.type == pygame.MOUSEBUTTONUP:
				for widget in Widget.widgets.values():
					widget.mouseReleased()
			if event.type == pygame.MOUSEBUTTONDOWN:
				for widget in Widget.widgets.values():
					widget.mousePressed()
			if event.type == pygame.MOUSEMOTION:
				for widget in Widget.widgets.values():
					widget.mouseMoved()
