/*
 * Image Processing based Gesture-controlled Arduino Home Automation Demonstration
 * 
 * Anmol Singh and Rian Borah, Delhi Public School, RK Puram
 * 
 * Program 1: Master Arduino Uno
 * 
 */
 
#include <SPI.h>  
#include <Pixy.h>
#include <Wire.h>
int slaveAddress = 9;
Pixy pixy;
bool b = 0;
void setup()
{
  Wire.begin();
  Serial.begin(9600);
  pixy.init();
  pixy.setLED(200, 200, 200);
}

void loop()
{ 
while(1){
  getData();
  while(Serial.available()){
  char c = Serial.read();
  if (c == '+'){
  Wire.beginTransmission(9);
  Wire.write('+'); 
  Wire.endTransmission();
  }
 else if(c == '-'){
  Wire.beginTransmission(9);
  Wire.write('-'); 
  Wire.endTransmission(); 
 } 
 else if(c == 'x'){
  Wire.beginTransmission(9);
  Wire.write('x'); 
  Wire.endTransmission();
  b = 1;
  break;
 }
  getData();
}
if(b == 1){
  b  = 0;
  break;
}
}
delay(100);
Serial.println("Stop");
Serial.readString();
Serial.flush();
delay(500);
}
void getData(){
    static int i = 0;
  int j;
  uint16_t blocks;
  char buf[32]; 
  blocks = pixy.getBlocks();
  if (blocks)
  {
    i++;
    int X = 0;
    int Y = 0;
    int counter = 0;
      for (j=0; j<blocks; j++)
      {
        X += pixy.blocks[j].x;
        Y += pixy.blocks[j].y;
        counter++;
      }
      X = (int) X/counter;
      Y = (int) Y/counter;
      Serial.print("0\t");
      Serial.print((String) X);
      Serial.print('\t');
      Serial.print((String) Y);
      Serial.println();
}
}
