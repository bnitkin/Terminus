#!/usr/bin/python2
# Jan 2014
# Ben Nitkin
# 
# Configuration file
# Single file for all config variables used in the base station. 


#Colors
from pygame import Color
WHITE = Color(255, 255, 255, 255)
BLACK = Color(  0,   0,   0, 255)
RED =   Color(255,   0,   0, 255)
GREEN = Color(  0, 255,   0, 255)
BLUE  = Color(  0,   0, 255, 255)

##UI Settings
WIDGET_WIDTH = 200
WIDGET_HEIGHT = 200
WIDGET_RADIUS = 90

DIAL_FILL = WHITE
DIAL_BORDER = BLACK

TICK_COLOR = BLACK
CENTER_BORDER = BLACK
CENTER_VAL = 100
CENTER_SAT = 100

LIGHT_RADIUS = 35

#A gauge's color changes depending on its value, for easier reading.
CENTER_HUE_NORMAL = 112
CENTER_HUE_DANGER = 0
NEEDLE_FILL = Color(0, 10, 81, 255)
NEEDLE_BORDER = BLACK

CENTER_RADIUS = 15
NEEDLE_RADIUS = 70

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 5

BUTTON_BORDER_1 = BLACK
BUTTON_BORDER_2 = Color(230, 230, 230)
BUTTON_NORMAL = Color(192, 192, 192)
BUTTON_HOVER = Color(170, 170, 170)
BUTTON_PRESS = Color(120, 120, 120)

TEXTBOX_WIDTH = 200
TEXTBOX_HEIGHT = 100
TEXTBOX_TEXT_BORDER = 10
TEXTBOX_TEXT_HEIGHT = 40
TEXTBOX_FILL = WHITE
TEXTBOX_BORDER = BLACK
TEXTBOX_TITLE_COLOR = WHITE

MAP_FILL = Color('#7AFF83')
MAP_MARGIN = 5
MAP_BORDER = BLACK
FEATURE_SIZE = 5 #Radius of features on maps.
TRACK_COLOR = BLACK
RESIZE_AREA = 0.5 #The width and height of the screen occupied by data immediately after a resize.
MAX_AREA = 0.9 #The fraction of the map usable by data. 0.9 sets a 10% edge buffer, and resizes when the buffer's violated.
BORDER_THICKNESS = 4

TICKS = 8
TICK_LENGTH = 10
LABEL_INSET = 25
DIGITAL_FROM_BOTTOM = 50
TITLE_FROM_BOTTOM = 65

SCALE_START = 3.1415* 1/3
SCALE_END =   3.1415* 5/3
SCALE_RANGE = SCALE_END - SCALE_START

WARN_BORDER = Color(142, 3, 0, 255)
WARN_FILL = Color(194, 5, 0, 255)
WARN_TEXT = WHITE

#Fonts
LABEL_NAME = 'res/AlteHaasGroteskRegular.ttf'
LABEL_SIZE = 12
TITLE_NAME = 'res/imagine_font.ttf'
TITLE_SIZE = 13
DIGITAL_NAME = 'res/digital_counter_7.ttf'
DIGITAL_SIZE = 30
FONT_COLOR = BLACK
DIGITAL_COLOR = Color(116, 4, 0, 255)

##Frontend settings
TITLE="Optimus' Base Station - Team Terminus - 2014"
TITLE_ICON = 'res/terminus.jpg'
BACKGROUND = Color(26, 26, 26)

FRAMERATE = 30

GRIDDING = 98
MAX_VEL = 2 #Max velocity, m/s
MAX_TURN = 2

#Rangefinder warning distances
RANGE_MIN = 1 #Red closer than this (m)
RANGE_MAX = 5 #Green further than this

##Serial settings
BAUDRATE = 115200
PORT = '/dev/ttyUSB0'
TIME_WRITE = 50 #ms; Maximum time to spend writing to serial per loop. (higher values fill read buffer)
TIME_MIN = 70 #ms; Minimum time for a read/write serial loop (higher values reduce CPU)
RATE_AVG = 20 #Number of samples to use for rate averaging.

#States
UNKNOWN = 0
READY = 1
BUSY  = 2
