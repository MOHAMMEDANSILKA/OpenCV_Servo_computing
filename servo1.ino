#include <ESP32Servo.h>

#define PAN_PIN 12 // Pin for Pan Servo
#define TILT_PIN 13 // Pin for Tilt Servo

Servo panServo; // Create servo object for pan

Servo tiltServo; // Create servo object for tilt

void setup() {
    // Attach the servo to its respective pin
    panServo.attach(PAN_PIN, 500, 2400); // Attach pan servo with min/max pulse width
    tiltServo.attach(TILT_PIN, 500, 2400); // Attach tilt servo with min/max pulse width

    Serial.begin(115200); // Start serial communication for debugging
}

void loop() {
    // Sweep Pan Servo from 0 to 180 degrees
    for (int pos = 0; pos <= 180; pos += 1) {
        panServo.write(pos); // Move to position 'pos'
        delay(15); // Wait for the servo to reach the position
    }

    // Sweep Pan Servo back from 180 to 0 degrees
    for (int pos = 180; pos >= 0; pos -= 1) {
        panServo.write(pos); // Move to position 'pos'
        delay(15); // Wait for the servo to reach the position
    }

    // Sweep Tilt Servo from 0 to 180 degrees
    for (int pos = 0; pos <= 180; pos += 1) {
        tiltServo.write(pos); // Move to position 'pos'
        delay(15); // Wait for the servo to reach the position
    }

    // Sweep Tilt Servo back from 180 to 0 degrees
    for (int pos = 180; pos >= 0; pos -= 1) {
        tiltServo.write(pos); // Move to position 'pos'
        delay(15); // Wait for the servo to reach the position
    }
}
