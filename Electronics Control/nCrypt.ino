
/*
 * Image Processing based Gesture-controlled Arduino Home Automation Demonstration
 * 
 * Anmol Singh and Rian Borah, Delhi Public School, RK Puram
 * 
 * Program 2: Slave Arduino Mega 2560
 * 
 */
 
// _____________________________

#include <Wire.h>

#include <SparkFun_TB6612.h> 

#define AIN1 22 

#define AIN2 24

#define PWMA 5

#define STBY 23

const int offsetA = 1;

Motor motor1 = Motor(AIN1, AIN2, PWMA, offsetA, STBY);

volatile int counter = 0;

// _____________________________

int led1 = 53;

int led2 = 52;

int led3 = 50;

int led4 = 51;

// _____________________________

int latchPin = 39;

int clockPin = 37;

int dataPin = 38;

// _____________________________

int R = 2;

int G = 3;

int B = 4;

// _____________________________

// Brightness Control (first two) or Toggle Control (last two)

char deviceArray[5] = {'L', 'M', 'R', 'S', 'B'};
//
int numEffectiveStates = 5;

//char deviceArray[3] = {'L', 'M', 'R'};
//
//int numEffectiveStates = 3;  

int deviceID = 0;

// _____________________________

int currentBrightness = 50;

int currentSpeed = 20;

int currentMode = 1;

int defaultLEDStep = 20;

int defaultMotorStep = 5;

int registerBrightness = 200;

int previousBrightness = 0;

int previousSpeed = 0;

// _____________________________

void setup() {
  // put your setup code here, to run once:

  Wire.begin(9);

  pinMode(R, OUTPUT);
  
  pinMode(G, OUTPUT);
  
  pinMode(B, OUTPUT);
  
  pinMode(18, INPUT);

  pinMode(led1, OUTPUT);

  pinMode(led2, OUTPUT);

  pinMode(led3, OUTPUT);
  
  pinMode(led4, OUTPUT);
  
  pinMode(13, OUTPUT);
  
  digitalWrite(13, LOW);
  
  attachInterrupt(digitalPinToInterrupt(18), changeState, RISING);

  changeState();

  pinMode(latchPin, OUTPUT);

  pinMode(dataPin, OUTPUT);  
  
  pinMode(clockPin, OUTPUT);

  pinMode(6, OUTPUT);

  analogWrite(6, registerBrightness);

  Serial.begin(9600);

  Wire.onReceive(receiveEvent);

}

void loop() {

while(deviceID == 0) {

  resetMotor();

  resetLights();

  Serial.println("Controlling RGB LED");

  
}

while(deviceID == 1) {

  resetRGBLED();

  resetLights();

  Serial.println("Controlling Motor");
  
}

while(deviceID >= 2) {

  resetRGBLED();

  resetMotor();

  Serial.println("Controlling Lights");
  
}

}

void changeState(){

  if((counter % numEffectiveStates) == 0){
  
    digitalWrite(led1, HIGH);
    
    digitalWrite(led2, LOW);
    
    digitalWrite(led3, LOW);

    digitalWrite(led4, LOW);
  
  }
  
  else if((counter % numEffectiveStates) == 1){
  
    digitalWrite(led1, LOW);
    
    digitalWrite(led2, HIGH);
    
    digitalWrite(led3, LOW);
    
    digitalWrite(led4, LOW);
  
  }
  
  else if ((counter % numEffectiveStates) == 2){

    if(numEffectiveStates == 3){

        digitalWrite(led1, LOW);
    
        digitalWrite(led2, LOW);
    
        digitalWrite(led3, HIGH);
    
        digitalWrite(led4, HIGH);
      
    }

    else {

      digitalWrite(led1, LOW);
    
      digitalWrite(led2, LOW);
    
      digitalWrite(led3, HIGH);
    
      digitalWrite(led4, LOW);
      
    }
  
    
  }

  else if ((counter % numEffectiveStates) == 3){
  
    digitalWrite(led1, LOW);
    
    digitalWrite(led2, LOW);
    
    digitalWrite(led3, LOW);
    
    digitalWrite(led4, HIGH);
  
  }
  
  else {
  
    digitalWrite(led1, LOW);
    
    digitalWrite(led2, LOW);
    
    digitalWrite(led3, HIGH);
    
    digitalWrite(led4, HIGH);
  }
 
  counter += 1;

  deviceID = (counter - 1) % numEffectiveStates;  

}

void changeRGBLEDBrightness(int newBrightness) {

  if(newBrightness > 255) {

    newBrightness = 255;    

  }

  else if(newBrightness < 0) {

    newBrightness = 0;  
  
  }  

  analogWrite(R, newBrightness);

  analogWrite(G, newBrightness);

  analogWrite(B, newBrightness);

}

int mapSpeed(int s){

  return s * 60/78;

}

int changeMotorSpeed(int newSpeed) {

  if(newSpeed > 255){

    newSpeed = 255;
    
  }

  else if(newSpeed < 0){

    newSpeed = 0;
    
  }

  currentSpeed = newSpeed;
  
  motor1.drive(mapSpeed(newSpeed));

}

void setLightingMode(int mode){

  if(numEffectiveStates == 3) {

  if(mode == 0) {

    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0);

    digitalWrite(latchPin, HIGH);
  
  }

  else if(mode == 1) {

    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0b11110000);

    digitalWrite(latchPin, HIGH);

  }  

  else if(mode == 2) {

    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0b00001111);

    digitalWrite(latchPin, HIGH);

  }

  else {

    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0b11111111);

    digitalWrite(latchPin, HIGH);

  }

  }

  else {

    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0);

    digitalWrite(latchPin, HIGH);

    if(mode > 255){

      mode = 255;
      
    }

    else if(mode < 0){

      mode = 0;
      
    }

    if(deviceID == 2){

    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0b11110000);

    digitalWrite(latchPin, HIGH);

    }

    else if (deviceID == 3){

      
    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0b00001111);

    digitalWrite(latchPin, HIGH);        
      
    }

    else {
      
    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0b11111111);

    digitalWrite(latchPin, HIGH);
     
  }

    analogWrite(6, mode);

    Serial.println(mode);
  
  }

}

void transferControl(char change) {

  Serial.println(deviceID);

  if(deviceArray[deviceID] == 'L') {

      if(change == '+'){

        currentBrightness += defaultLEDStep;

      }

      else if(change == '-'){

        currentBrightness -= defaultLEDStep; 
    
      }

      changeRGBLEDBrightness(currentBrightness);

  }

  else if(deviceArray[deviceID] == 'M') {

      if(change == '+'){

        currentSpeed += defaultMotorStep;

      }

      else if(change == '-'){

        currentSpeed -= defaultMotorStep; 
    
      }

      changeMotorSpeed(currentSpeed);

  }

  else {

    if(numEffectiveStates == 3){

     if(change == '+'){

        currentMode += 1;

      }

      else if(change == '-'){

        currentMode -= 1; 
    
      }

      currentMode = currentMode % 4;

      setLightingMode(currentMode);

  }

  else {

     if(change == '+'){

        registerBrightness -= defaultLEDStep;

      }

      else if(change == '-'){

        registerBrightness += defaultLEDStep; 
    
      }

      setLightingMode(registerBrightness);
    
    }
    
  }

}

void resetMotor(){
  
  motor1.drive(0);

}

void resetRGBLED(){

  analogWrite(R, 0);

  analogWrite(G, 0);

  analogWrite(B, 0);
  
}

void resetLights(){

    digitalWrite(latchPin, LOW);

    shiftOut(dataPin, clockPin, LSBFIRST, 0);

    digitalWrite(latchPin, HIGH);

    delay(20);
  
}

void receiveEvent(){

  byte a = Wire.read();

  Serial.println(a);

  if(a == 45){

    transferControl('-');
    
  }

  else if(a == 43){

    transferControl('+');
    
  }

  else {

    transferControl('.');
    
  }
  
}

