#include <Servo.h>

Servo servo;
void setup() {
  servo.attach(5);
  Serial.begin(9600);
  servo.write(0);
  delay(2000);
}

char var;
String input = "";

void loop() {
  servo.write(180);
  delay(3000);
  servo.write(0);
  delay(3000);


//  if (Serial.available()) { 
//    while(Serial.available()>0){
//      var=Serial.read();
//      input+=var;
//    }
//  }

}
