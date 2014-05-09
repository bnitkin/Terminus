#include <QueueList.h>
#include <PID_v1.h>
#include <Servo.h>
#include <Encoder.h>

//Pin constants
static int reedL0 = 10, reedL1 = 11, reedR0 = 12, reedR1 = 13;
static int leftMotor = 6, rightMotor = 7;

//PID Variables
double leftTarget = 1,  leftSpeed = 0,  leftOutput = 0,
       rightTarget = 1, rightSpeed = 0, rightOutput = 0; //PID control

//PID Constants
static float lkp = 9.3160*90/6, lki = 0, lkd =  10.1867*90/6; //Either 90/6 or 180/6 to convert Larry's PID values to an angular value.
static float rkp = 9.3160*90/6, rki = 0, rkd =  10.1867*90/6;

//Safety maxima.
static int maxAngle = 90; //The maximum angle to drive the controllers at.
static int maxSpeed = 4; //Maximum speed to drive at.

//PID Controllers
PID leftMotorPID(&leftSpeed,   &leftOutput,  &leftTarget,  lkp, lki, lkd, DIRECT); //DIRECT vs REVERSE determines direction.
PID rightMotorPID(&rightSpeed, &rightOutput, &rightTarget, rkp, rki, rkd, DIRECT); 

//Optical Encoders
Encoder leftenc(reedL0, reedL1); //For reading encoders
Encoder rightenc(reedR0, reedR1);

//Optical Encoder SupportStuff
QueueList<long> leftEncoderTimes, rightEncoderTimes, leftEncoderPos, rightEncoderPos;
int leftenclast = -999, rightenclast = -999;
static int rollingAverage = 9; //# of samples in RPM reading //Bad pun.

//Motor Drivers
Servo leftmotor; //For writing motor speeds
Servo rightmotor;


void wheelSetup()
{
  //Init serial
  Serial.begin(9600);
  
  //Init servo outputs
  rightmotor.attach(rightMotor);
  leftmotor.attach(leftMotor);
  
  //Init PID
  leftMotorPID.SetMode(AUTOMATIC);
  rightMotorPID.SetMode(AUTOMATIC);
  leftMotorPID.SetSampleTime(50);
  rightMotorPID.SetSampleTime(50);
  leftMotorPID.SetOutputLimits(-maxAngle,  maxAngle);
  rightMotorPID.SetOutputLimits(-maxAngle, maxAngle);
  
  //Init queues
  for (int i = 0; i < rollingAverage; i++) {
    leftEncoderTimes.push(micros());
    rightEncoderTimes.push(micros());
    leftEncoderPos.push(0);
    rightEncoderPos.push(0);
  }
}

void wheelLoop() {
  //Speed threshold. Safety measure.
  leftTarget = min(leftTarget, maxSpeed);
  rightTarget = min(rightTarget, maxSpeed);
  
  //PID control
  leftMotorPID.Compute();
  rightMotorPID.Compute();
  
  leftmotor.write(leftOutput+90);
  rightmotor.write(rightOutput+90);
  
  //Constant control (debug)
  //leftmotor.write(115);
  //rightmotor.write(115);
  
  
  //Encoder updates:      micrometers/tick   /    (microseconds / ticks)
  rightSpeed = -4888.44 / ((micros() - rightEncoderTimes.peek()) / (float)(rightenc.read() - rightEncoderPos.peek()));
  leftSpeed =   4888.44 / ((micros() -  leftEncoderTimes.peek()) / (float)(leftenc.read() - leftEncoderPos.peek()));

  if (leftenc.read() != leftenclast) {
    leftenclast = leftenc.read();
    
    leftEncoderTimes.push(micros());
    leftEncoderPos.push(leftenc.read());
    leftEncoderTimes.pop();
    leftEncoderPos.pop();
  }
  
  //Simple R-Code implementation.
  Serial.println("prime,R37");
  Serial.println(leftSpeed);
  Serial.println(0);                   
}

