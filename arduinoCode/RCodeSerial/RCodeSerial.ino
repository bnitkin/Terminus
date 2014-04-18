

void setup()
{
  Serial.begin(9600);
}
volatile String command;

void loop()
{
  //READ SERIAL
  // if there's any serial available, read a line into a string "command"
  // Parse it for three lines, the typical set expected from the computer
  if(Serial.available() > 0){
    command = Serial.readStringUntil('\n');
    if(command.substring(0,2) = "R34"){
    //  "R34 1.2 0.3" to speedOverall = 1.2m/s and turnrate = 0.3rad/s
    }
    if(command.substring(0,2) = "R35" {
    //  "R35 1.23" to speedLeft = 1.23m/s  
    }
    if(command.substring(0,2) = "R34"){
    //  "R36 2.35" to speedRight = 2.35m/s
    }
  }
    //Form strings and send them for each output
    #include <reedv4Optical.ino> //include encoder
    #include <rangefinders2.ino> //include rangefinders
    
    
  }
