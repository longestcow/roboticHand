#include <Servo.h>
#include <List.hpp>


List<String> list(true);
Servo servo;
void setup() {
  servo.attach(5);
  servo.write(0);
  
  Serial.begin(9600);
}

String input = "default", allinput = "";
char var;
void loop() {
//  servo.write(180);
//  delay(2000);
//  servo.write(0);
//  delay(2000);

  if (Serial.available() > 0) {
    input = Serial.readStringUntil('\n');
    allinput+=input+" ";
    clearBuffer();
  }
  if(allinput!="")
    Serial.println(allinput);

}

void clearBuffer(){
  while(Serial.available() > 0)
    Serial.read();
}
