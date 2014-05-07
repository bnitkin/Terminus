#!/usr/bin/python2
# Jan 2014
# Ben Nitkin
# 
# Configuration file
# Single file for all config variables used in the base station. 

from pygame import Color
import sys

#Colors
WHITE = Color(255, 255, 255, 255)
BLACK = Color(  0,   0,   0, 255)
RED =   Color(255,   0,   0, 255)
GREEN = Color(  0, 255,   0, 255)
BLUE  = Color(  0,   0, 255, 255)

##UI Settings
WIDGET_WIDTH = 200
WIDGET_HEIGHT = 200
WIDGET_RADIUS = 90

#Basic colors
DIAL_FILL = WHITE
DIAL_BORDER = BLACK

#Center color dial config
CENTER_BORDER = BLACK
CENTER_VAL = 100
CENTER_SAT = 100
CENTER_HUE_NORMAL = 112
CENTER_HUE_DANGER = 0
CENTER_RADIUS = 15
LIGHT_RADIUS = 35

#Needle config (compass, speedo, heading)
NEEDLE_FILL = Color(0, 10, 81, 255)
NEEDLE_BORDER = BLACK
NEEDLE_RADIUS = 70

#Settings for minor ticks on speedo etc
TICKS = 8
TICK_LENGTH = 10
TICK_COLOR = BLACK
SCALE_START = 3.1415* 1/3
SCALE_END =   3.1415* 5/3
SCALE_RANGE = SCALE_END - SCALE_START

#Text spacing for speedo, compass, etc
LABEL_INSET = 25
DIGITAL_FROM_BOTTOM = 50
TITLE_FROM_BOTTOM = 65

#Colors for warning overlays
WARN_BORDER = Color(142, 3, 0, 255)
WARN_FILL = Color(194, 5, 0, 255)
WARN_TEXT = WHITE

#Button config
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 5

BUTTON_BORDER_1 = BLACK
BUTTON_BORDER_2 = Color(230, 230, 230)
BUTTON_NORMAL = Color(192, 192, 192)
BUTTON_HOVER = Color(170, 170, 170)
BUTTON_PRESS = Color(120, 120, 120)

#Textbox config
TEXTBOX_WIDTH = 200
TEXTBOX_HEIGHT = 100
TEXTBOX_TEXT_BORDER = 10
TEXTBOX_TEXT_HEIGHT = 40
TEXTBOX_FILL = WHITE
TEXTBOX_BORDER = BLACK
TEXTBOX_TITLE_COLOR = WHITE

#Map config
MAP_FILL = Color('#7CFA4C')
MAP_MARGIN = 5
MAP_BORDER = BLACK
SCALE_COLOR = BLACK
FEATURE_SIZE = 5 #Radius of features on maps.
TRACK_COLOR = BLACK
RESIZE_AREA = 0.5 #The width and height of the screen occupied by data immediately after a resize.
MAX_AREA = 0.9 #The fraction of the map usable by data. 0.9 sets a 10% edge buffer, and resizes when the buffer's violated.
SCALE_SIZE = 0.15 #The rough size of the scale, as a fraction of map width.
BORDER_THICKNESS = 4
MAX_MOVE = 1000 #Maximum offset between sequential points on map, m.


#Fonts
LABEL_NAME = sys.path[0]+'/res/AlteHaasGroteskRegular.ttf'
LABEL_SIZE = 12
TITLE_NAME = sys.path[0]+'/res/imagine_font.ttf'
TITLE_SIZE = 13
DIGITAL_NAME = sys.path[0]+'/res/digital_counter_7.ttf'
DIGITAL_SIZE = 30
FONT_COLOR = BLACK
DIGITAL_COLOR = Color(116, 4, 0, 255)

##Frontend settings
TITLE="Optimus' Base Station - Team Terminus - 2014"
TITLE_ICON_WIN = sys.path[0]+'/res/primesmiley.gif'
TITLE_ICON_MAC = sys.path[0]+'/res/primebody.gif'
BACKGROUND = Color(26, 26, 26)

FRAMERATE = 30

GRIDDING = 98
MAX_VEL = 2 #Max velocity, m/s; used in teleop mode.
MAX_TURN = 2

#Rangefinder warning distances
RANGE_MIN = 1 #Red closer than this (m)
RANGE_MAX = 5 #Green further than this

##Serial settings
BAUDRATE = 115200
PORT = '/dev/ttyUSB1'
TIME_WRITE = 50 #ms; Maximum time to spend writing to serial per loop. (higher values fill read buffer)
TIME_MIN = 70 #ms; Minimum time for a read/write serial loop (higher values reduce CPU)
RATE_AVG = 20 #Number of samples to use for rate averaging.
