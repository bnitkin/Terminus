int analogPin0 = A0;     // rangefinder L connected to pin A0
int angalogPin1=  A1;    //rangefiner C connected to pin A1
int analogPin2 = A2;     //rangefinder R connected to pin A2
int RangeL = 0;           // variable to store rangefinder L voltage
int RangeC = 0;           // variable to store rangefinder C voltage
int RangeR = 0;           // variable to store rangefinder R voltage

void setup()
{
  Serial.begin(9600);          //  setup serial
}

void loop()
{
  RangeL = analogRead(analogPin0);    // read analog pin A0
  RangeC = analogRead(analogPin1);    // read analog pin A1
  RangeR = analogRead(analogPin2);    // read analog pin A2
  Serial.print("Left Voltage")        // print left rangefinder header
  Serial.println(RangeL);             // print L voltage value to serial
  Serial.print("Center Voltage");     // print center rangefinder header
  Serial.println(RangeC);             // print C voltage value to serial
  Serial.print("Right Voltage");      // print center rangefinder header
  Serial.println(RangeR);             // print C voltage value to serial
  delay(10);                          // delay 10 milliseconds before the next reading:
}
