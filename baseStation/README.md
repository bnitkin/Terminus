#Base Station Readme
##Introduction
The base station provides telemetry from the robot via an an XBee serial radio link. 
This telemetry includes an image and map, GPS fix, heading and speed, radio metrics,
and a few others. 

The station can also bring the robot in and out of autonomous mode, poweroff the robot, 
and perform an E-Stop. (There are two other E-Stops: one a radio link and a button on the robot.)

If a joystick is attached, the base station can drive the robot in teleoperated mode.

##Interface
The interface is organized by functionality. The right side is dedicated to GPS, 
while the left groups sensors. Large widgets (image, map) are on top.

Many widgets are color coded and change colors from green to red. Green either means 'good' or 'on';
red is either 'warning' or 'off'.

The base station mostly provides a readout, but buttons and some widgets respond to clicks:
- Teleop / Autonav: Switches between autonav and teleoperated mode. 
- E-Stop: Immediately stops robot.
- Shutdown: Stops the robot and powers down the ROS master. 
- Prtscr: Saves a screenshot to baseStation/screenshots.
- Map: Clicking will remove the first half of the track and redraw the map. Repeated clicks clear the track.

##Bandwidth management
The XBee link has limited bandwidth and imperfect transmission reliability. The 
base station will enable and disable widgets based on availiable bandwidth. 
Disabling widgets cuts down on total radio traffic and prioritizes important information.

##File organization
- buttons.py functions called on button click.
- config.py settings for the base station: colors, geometries, speeds, etc. (all other files draw on the settings saved here)
- frontend.py the main program: populates widgets, starts serial and joystick, and passes pyGame events around.
- link.py serial cache: Sits between the XBee and the RCode interpreter to buffer data. 
(PySerial's built-in buffer is only 3k and overflows in about 1/6s.) 
- rcode.py pulls rcodes from the link, parses them, and sets the relevant widget(s)
- screenshots/ holds any screenshots taken from the base station. 
- res/ contains all non-code files (fonts, icons, images, etc)
