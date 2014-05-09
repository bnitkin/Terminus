#include <QueueList.h>
#include <PID_v1.h>
#include <Servo.h>
#include <Encoder.h>

//Pin constants
static int reedL0 = 10, reedL1 = 11, reedR0 = 12, reedR1 = 13;
double leftSpeed = 0, rightSpeed = 0;




//Optical Encoders
Encoder leftenc(reedL0, reedL1); //For reading encoders
Encoder rightenc(reedR0, reedR1);

//Optical Encoder SupportStuff
QueueList<long> leftEncoderTimes, rightEncoderTimes, leftEncoderPos, rightEncoderPos;
int leftenclast = -999, rightenclast = -999;
static int rollingAverage = 9; //# of samples in RPM reading //Bad pun.

void wheelSetup()
{
  //Init serial
  Serial.begin(9600);
 
  //Init queues
  for (int i = 0; i < rollingAverage; i++) {
    leftEncoderTimes.push(micros());
    rightEncoderTimes.push(micros());
    leftEncoderPos.push(0);
    rightEncoderPos.push(0);
  }
}

void wheelLoop() {
  
  
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
  
    if (rightenc.read() != rightenclast) {
    rightenclast = rightenc.read();
    rightEncoderTimes.push(micros());
    rightEncoderPos.push(rightenc.read());
    rightEncoderTimes.pop();
    rightEncoderPos.pop();
  }
  
  //Simple R-Code implementation.
  Serial.println("prime,R37");
  Serial.println(leftSpeed);
  Serial.println(rightSpeed);                   
}

