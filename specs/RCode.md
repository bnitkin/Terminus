#Robot-Code Draft V
##Overview
R-code standardizes inter-device communication on the robot. R-Code behaves on a master-and-slave framework. 
The master transmits short codes to either request information or apply settings, and the slave constantly 
sends the requested set of data. The architecture responds to bandwidth changes by changing state; 
shorthand for a set of enabled data.

R-Code is roughly based on the G-code of the Reprap and other CAM tools. Two R-code links exist 
on the robot. The base station acts as a master to a receiving node on the robot laptop. A separate node
onboard the robot commands the Arduino. In each case, the master (brain) sends a request that's executed 
by the slave (body). 
##Communication
R-Code is an asynchronous protocol. The master sends out codes to either transmit data (wheel speeds) 
or adjust data transmission (state changes). The slave periodically reads communications from the master 
and constantly transmits all enabled data, based on current state.

R-Codes consist of the letter R followed by two numbers, 00 through 99. Expanding into alpha (a-z) will 
provide additional codes if needed. Codes refer to pieces of data, so have different meanings depending 
on direction. For instance, the master sends *R07 1* to set mode. The robot provides its current mode with 
the same code: 
```
prime,R07\n1\n
```

The format varies slightly between the master and slave. For the master, arguments are space-delimited, 
and reside on the same line as the code. The following code transmits code 33 with arguments 1.0 and 1.1.
```
R33 1.0 1.1
```

The slave codes look slightly different to account for the variety of data the slave sends. If a valid 
control code randomly appeared in the data transmission, flow control would break. The robot sends the 
identifier 'prime,' followed by the code for the data it's transmitting. 
```
prime,<R-code>
```
Newline-delimited data follows. Another flag marks the end of the current data transmission and start of the next. 
##States
The robot-base station link has 5 states, 1-5. (The wired Arduino link shouldn't have 
bandwidth issues, so states aren't defined.) The following is a list of codes transmitted 
in each state; it's tuned to the base station's needs.

1)
 - R00 (alive)

2) 
- Everything from 1 and:
- R07 (autonomous)
- R37 (actual twist)
- R53 (heading)

3) 
- Everything from 2 and:
- R60 (left range)
- R61 (center range)
- R62 (right range)
- R16 (uptime)

4) 
 - Everything from 3 and:
 - R26 (current waypoint)
 - R40 (position)
 - R41 (accuracy)
 - R42 (num satellites)

5) 
- Everything from 4 and:
- R70 (image)

##Notes
For signal processing, JPEG images always start with 0xFFD8 and end with 0xFFD9. 
JPEG's are likely to be the heaviest data that moves across the radio link.

The regular expression *^prime,R[0-9][0-9]$* matches flags and only flags. 

ROS is natively metric, so R-codes will be, too. Ranges are in meters and speeds in m/s.

##Sample Session
Comments are marked by #'s

|Master Transmission	|Slave Transmission	
|---|---
|R07 1 #Set robot to state 1	|prime,R13
|R37 1.2, 0.2 #Set twist	12.2|12.2
||	prime,R16
||	340.2
||	prime,R53
||	192	
||	prime,R07 #Robot is in state 1 – confirmed.
||	1
||	prime,R00
||	prime,R00
||prime,R00
||...
