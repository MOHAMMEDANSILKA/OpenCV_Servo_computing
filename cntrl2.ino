#include <ESP32Servo.h>

Servo panServo;
Servo tiltServo;

const int panPin = 12;
const int tiltPin = 13;

int panAngle = 90;
int tiltAngle = 90;

void setup() {
  Serial.begin(115200);
  panServo.attach(panPin);
  tiltServo.attach(tiltPin);
  
  panAngle = constrain(panAngle, 0, 180);
  tiltAngle = constrain(tiltAngle, 30, 120);
  
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.startsWith("PAN:")) {
      panAngle = command.substring(4).toInt();
      panAngle = constrain(panAngle, 0, 180);
      panServo.write(panAngle);
    }
    else if (command.startsWith("TILT:")) {
      tiltAngle = command.substring(5).toInt();
      tiltAngle = constrain(tiltAngle, 30, 120);
      tiltServo.write(tiltAngle);
    }
  }
}
