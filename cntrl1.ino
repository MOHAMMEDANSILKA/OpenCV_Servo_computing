#include <ESP32Servo.h>

Servo panServo;
Servo tiltServo;

const int panPin = 12;
const int tiltPin = 13;

int panAngle = 90;
int tiltAngle = 90;
//setup
void setup() {
  Serial.begin(115200);
  panServo.attach(panPin);
  tiltServo.attach(tiltPin);
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.startsWith("PAN:")) {
      panAngle = command.substring(4).toInt();
      panServo.write(panAngle);
    }
    else if (command.startsWith("TILT:")) {
      tiltAngle = command.substring(5).toInt();
      tiltServo.write(tiltAngle);
    }
  }
}
