#include <QueueList.h>
#include <PID_v1.h>
#include <Servo.h>
#include <Encoder.h>

//Pinout constants
static int reedL0 = 10;
static int reedL1 = 11;
static int reedR0 = 12;
static int reedR1 = 13;

static int leftMotor = 6;
static int rightMotor = 7;

//Other constants
static double lkp = 1;
static double lki = 0;
static double lkd = .05;
static double rkp = 1;
static double rki = 0;
static double rkd = .05;

//Globals
double leftsetpoint = 0,  leftinput = 0,  leftoutput = 0,
       rightsetpoint = 0, rightinput = 0, rightoutput = 0; //PID control
       
PID leftMotorPID(&leftsetpoint, &leftinput, &leftoutput, lkp, lki, lpd, DIRECT); //DIRECT vs REVERSE determines direction.
PID rightMotorPID(&rightsetpoint, &rightinput, &rightoutput, rkp, rki, rpd, DIRECT);

Encoder leftenc(reedL0, reedL1); //For reading encoders
Encoder rightenc(reedR0, reedR1);

Servo leftmotor; //For writing motor speeds
Servo rightmotor;

QueueList<long> leftEncoderTimes, rightEncoderTimes;

int leftenclast = -999; //Encoder monitoring.
int lefttimelast = 0;
int rightenclast = -999;
int righttimelast = 0;

void setup()
{
  Serial.begin(9600);          //  setup serial
  rightmotor.attach(rightMotor);
  leftmotor.attach(leftMotor);
  leftmotorPID.SetMode(AUTOMATIC);
  rightmotorPID.SetMode(AUTOMATIC);
}

void loop() {
  //recalc pid
  leftmotorPID.Compute();
  rightmotorPID.Compute();
  leftmotor.write(leftoutput);
  rightmotor.write(rightoutput);
  
  //encoder handling
  if ((leftenc.read() != leftenclast)) {
    leftenclast = leftenc.read();
    String s = "left,";
    s += micros();
    s += ",";
    s += 15000000/(micros()-righttimelast); //RPM = 60sec/min*1000ms/sec* ?? rev/ms
    righttimelast = micros();
    Serial.println(s);
  }
  
  if ((rightenc.read() != rightenclast) && (rightenc.read()%18 == 0)) {
    rightenclast = rightenc.read();
    String s = "right,";
    s += millis();
    s += ",";
    s += 15000000/(micros()-righttimelast); //RPM = 60sec/min*1000ms/sec* ?? rev/ms
    righttimelast = micros();
    Serial.println(s);
  }
}


