#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27,16,2);
Servo servo;
void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.clear();         
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("waiting");
}

char var;
String input = "";

void loop() {
  if (Serial.available()) { 
    lcd.clear();
    while(Serial.available()>0){
      var=Serial.read();
      input+=var;
    }
    lcd.setCursor(0,0);
    lcd.print(input);
  }

}
