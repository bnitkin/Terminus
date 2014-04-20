//Rangefinder Pins
static int leftRangePin =  0;     // ***Check correct pin numbers***
static int centerRangePin= 1;
static int rightRangePin = 2;

static float rangeConstant = 0.01278;   // *** (3.3V/1024) / (6.4mV/in) * 0.0254 in/m
               
float rangeL = 0;           // variables to store rangefinder voltages
float rangeC = 0;          
float rangeR = 0;           

void rangeloop()
{
  rangeL = analogRead(leftRangePin)*rangeConstant;    
  rangeC = analogRead(centerRangePin)*rangeConstant; 
  rangeR = analogRead(rightRangePin)*rangeConstant;
  
  String L = "prime,R60\n";
  L = L+rangeL;
  String C = "prime,R61\n";
  C = C+rangeC;
  String R = "prime,R62\n";
  R = R+rangeR;
  Serial.println(L);
  Serial.println(C);
  Serial.println(R);
  delay(500);
}

