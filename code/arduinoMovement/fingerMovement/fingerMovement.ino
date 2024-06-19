#include <Servo.h>

String input = "default"; char var;

char fingers[] = "00000"; //contains the latest input from python
char cfingers[] = "00000"; //contains the current finger positions on the robot
int off[] = {0,180,0,180,0};
int on[] = {180,0,180,0,160};
//confirmed 11111
Servo servos[5];

void setup() {
  for(int i = 0; i<5; i++){
    servos[i].attach(i+2);
  }
  Serial.begin(9600);
  for(int i = 0; i<5; i++){
    servos[i].write(off[i]);
  }
}

void loop() {
  if (Serial.available() > 0) {
    input="";
    while(Serial.available() > 0) {
      var=(char) Serial.read();
      input+=var;
      delay(10);
    }
    input.trim();
    
    for(int i = 0; i<5; i++){
      fingers[i]=input.charAt(i);
    }
    
  }

  for(int i = 0; i<5; i++){
      if(fingers[i] != cfingers[i]){ 
        if(fingers[i]=='0'){
          servos[i].write(off[i]);
          cfingers[i]='0';
        }
        else {
          servos[i].write(on[i]);
          cfingers[i]='1';
        }
      }
  }
  
}
