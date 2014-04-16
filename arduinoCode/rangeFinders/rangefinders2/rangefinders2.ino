int analogPin0 = 0;     // rangefinder 1 (L) connected to pin 0
int analogPin1=  1;      //rangefinder 2 (C) connected to pin 1
int analogPin2=  2;      //rangefinder 3 (R) connected to pin 2
                       
int rangeL = 0;           // variables to store rangefinder voltages
int rangeC = 0;          
int rangeR = 0;           

void setup()
{
  Serial.begin(9600);          //  setup serial
}

void loop()
{
  rangeL = analogRead(analogPin0)*4.9/9.8;    // read analog pins, convert voltage to inches [units*(4.9mV/unit)*(1 inch/9.8mV)]
  rangeC = analogRead(analogPin1)*4.9/9.8; 
  rangeR = analogRead(analogPin2)*4.9/9.8;
  String L = "Left\t";
  L = L+rangeL;
  String C = "Center\t";
  C = C+rangeC;
  String R = "Right\t";
  R = R+rangeR;
  Serial.println(L);
  Serial.println(C);
  Serial.println(R);
  delay(100);
}
