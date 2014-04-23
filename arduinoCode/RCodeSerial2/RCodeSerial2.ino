

float speedTotal= 0;
float turnRate  = 0;
float speedLeft = 0;
float speedRight= 0;



void setup()
{
  Serial.begin(9600);
 /* rightmotor.attach(rightMotor);
  leftmotor.attach(leftMotor);
  leftmotorPID.SetMode(AUTOMATIC);
  rightmotorPID.SetMode(AUTOMATIC); */
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
      String total = command.substring(4,                       command.indexOf(" ", 4)-1);
            char carray[total.length() + 1]; //determine size of the array
            total.toCharArray(carray, sizeof(carray)); //put readStringinto an array
            float speedTotal = atof(carray);
      String turn = command.substring(command.indexOf(" ", 4)+1, command.length()      );
            char chararray[turn.length() + 1]; //determine size of the array
            turn.toCharArray(chararray, sizeof(chararray)); //put readStringinto an array
            float turnRate = atof(chararray);
    }
    if(command.substring(0,2) = "R35") {
      //  "R35 1.23" to speedLeft = 1.23m/s 
      command = command.substring(4,command.length());
      char carray[command.length() + 1]; //determine size of the array
      command.toCharArray(carray, sizeof(carray)); //put readStringinto an array
      float speedLeft = atof(carray);   

    }
    if(command.substring(0,2) = "R36") {
      //  "R36 2.35" to speedRight = 2.35m/s 
      command = command.substring(4,command.length());
      char carray[command.length() + 1]; //determine size of the array
      command.toCharArray(carray, sizeof(carray)); //put readStringinto an array
      float speedRight = atof(carray);
    }
    String speedReturnTotal = "Total ";
    speedReturnTotal = speedReturnTotal +speedTotal;
    Serial.println(speedReturnTotal);
    String Turn = "Turn ";
    Turn = Turn + turnRate;
    Serial.println(Turn);
    String Left = "Left ";
    Left = Left + speedLeft;
    Serial.println(Left);
    String Right = "Right ";
    Right = Right + speedRight;
    Serial.println(Right);
    delay(100);
  }
    //Call functions in tabs, which are our modules for the encoder and the rangefinders.
    rangeloop();

    
    
  }
