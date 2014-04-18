

float speedTotal
float turnRate
float speedLeft
float speedRight

void setup()
{
  Serial.begin(9600);
  rightmotor.attach(rightMotor);
  leftmotor.attach(leftMotor);
  leftmotorPID.SetMode(AUTOMATIC);
  rightmotorPID.SetMode(AUTOMATIC);
}

void loop()
{
  //READ SERIAL
  // if there's any serial available, read a line into a string "command"
  // Parse it for three lines, the typical set expected from the computer
  if(Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if(command.substring(0,2) = "R34") {
      //  "R34 1.2 0.3" to speedOverall = 1.2m/s and turnrate = 0.3rad/s
      speedTotal = float(command.substring(4,                       command.indexOf(" ", 4));
      turnRate =   float(command.substring(command.indexOf(" ", 4), command.length()      ));
    }
    if(command.substring(0,2) = "R35") {
      //  "R35 1.23" to speedLeft = 1.23m/s  
      speedLeft = float(command.substring(4,command.length());
    }
    if(command.substring(0,2) = "R36") {
      //  "R36 2.35" to speedRight = 2.35m/s
      speedRight = float(command.substring(4,command.length());
    }
  }
    //Call functions in tabs, which are our modules for the encoder and the rangefinders.
    rangeloop();
    encoderloop();
    
    
  }
