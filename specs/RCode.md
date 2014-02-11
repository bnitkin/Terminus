R##|Name|Details|Return data|Arg 1 (Return Data)|Arg 2|Sample data
R00|Keep-alive|Reset robot watchdog||||
R01|Kill|Software disable motors||||
R02|Power down|Power off laptop remotely||||
R03||||||
R04||||||
R05|Enable teleop|R05-R07 switch active control stations.||||
R06|Enable autonomous|Only one of the three control methods can be active at once.||||
R07|Mode|"Returns current mode (1=auto| 0=tele)"||0 or 1||
R08|State|Sets c||||
R09||||||
R10|Battery voltage|Retrieve battery voltage from robot|Volts|||22.4
R11||||||
R12||||||
R13|Current draw|"Measure onboard current| instantaneously"|"Amps, decimal"|||12.4
R14|Average current draw|Retrieve 1-minute average current draw|"Amps, decimal"|||0.5
R15||||||
R16|Time since boot|"ROS timestamp| measured in seconds"|Seconds|||354.78
R17||||||
R18||||||
R19||||||
R20|Add waypoint|Append waypoint to robot's navigation list||Latitude,Longitude|
R21|Reset waypoints|Clear navigation goal list||||
R22||||||
R23||||||
R24||||||
R25|Retrieve waypoints|Fetch navigation list from robot|List of waypoints|||30.45\n-50.34\n31.50\n-55.55
R26|Current waypoint|Fetch current waypoint only|Single waypoint|||30.45\n-50.34
R27|Next waypoint|Fetch next waypoint|Single waypoint|||30.45\n-50.35
R28|Planned route |Retrieve the route plotted by the Nav stack|10m or so of navigation path|||Unknown.
R29||||||
R30||||||
R31||||||
R32||||||
R33||||||
R34|Assigned twist|Retrieve target twist|Twist|||???
R35|Assigned left speed|Retrieve the robot's target speed|"Speed, m/s"|||1.23
R36|Assigned right speed|Retrieve the robot's target speed|"Speed, m/s"|||2.31
R37|Actual twist|Retrieve actual twist|Twist|||???
R38|Actual left speed|Retrieve actual wheel speed|"Speed, m/s"|||1.19
R39|Actual right speed|Retrieve actual wheel speed|"Speed, m/s"|||2.41
R40|Position|Retrieve GPS position|Coordinates|||30.45\n-50.34
R41|Accuracy,"GPS accuracy| as reported by the Arduino"|"Accuracy, in feet"|||6.2
R42|Number of satellites||Number of tracked satellites|||9
R43|Individual satellite strength||List of satellites and their strength|||2 1.3\n4 2.0 …
R44||||||
R45||||||
R46||||||
R47||||||
R48||||||
R49||||||
R50|Gyro rates|Measure all axes|"X| Y| and Z slew rates"|||1.23\n2.34\n3.45
R51|Acceleration|Measure all axes|"X| Y| and Z acceleration rates"|||1.23\n2.34\n3.46
R52|Magnometer|Measure all axes|"X| Y| and Z magnet readings"|||1.23\n2.34\n3.47
R53|Heading||"Heading| in degrees"|||243
R54||||||
R55||||||
R56||||||
R57||||||
R58||||||
R59||||||
R60|Left range|Retrieve range sensor's reading|"Range| meters"|||20
R61|Center range |Retrieve range sensor's reading|"Range| meters"|||200
R62|Right range|Retrieve range sensor's reading|"Range| meters"|||35
R63||||||
R64||||||
R65||||||
R66||||||
R67||||||
R68||||||
R69||||||
R70|Image size|Set image size||"Image width| pixels"|"Height| pixels"|640 480
R71|JPEG Quality|Set image quality||Quality (0-100)||25
R72||||||
R73||||||
R74||||||
R75|Fetch image|"Image comes from predetermined camera (Right| I think.)"|JPEG image|||<Raw JPEG bitstream>
R76|Fetch depthmap||???|||???
R77||||||
R78||||||
R79||||||
R80||||||
R81||||||
R82||||||
R83||||||
R84||||||
R85||||||
R86||||||
R87||||||
R88||||||
R89||||||
R90||||||
R91||||||
R92||||||
R93||||||
R94||||||
R95||||||
R96||||||
R97||||||
R98||||||
R99||||||
