//Andrew Kristof
//(Optimus)' Tachometer
//Read the state of a switch and calculate the wheel velocity based upon time

int digitalPin0 = 30;    // reed switch 1 connected to pin 30
int capture;          //variable to store when the switch is activated
int captureOld;      //old capture state
long startTime;      //variable to store when switch is triggered
long elapsedTime;    //variable to hold how long switch took to trigger twice

void setup()
{
  Serial.begin(9600);          //  setup serial
  pinMode(digitalPin0,INPUT);  // set pin to be input
}

void loop()
{
  capture = digitalRead(digitalPin0);    // read pin 30 state
  if (capture=HIGH&&captureOld=LOW){
    startTime=milis();  //note the time this happened
    captureOld=capture;  //transition from new to old
  }
  else if (capture=HIGH&&captureOld=HIGH){
    
  Serial.println(reed1);              // print reed 1 value to serial
}
