#include <Servo.h>


Servo servos[5];
void setup() {
  for(int i = 0; i<5; i++){
    servos[i].attach(i+1);
  }
  Serial.begin(9600);
}

String input = "default"; char var;

char fingers[] = "00000"; //contains the latest input from python
char cfingers[] = "00000"; //contains the current finger positions on the robot

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
          servos[i].write(0);
          cfingers[i]='0';
        }
        else {
          servos[i].write(180);
          cfingers[i]='1';
        }
      }
  }
  
}
