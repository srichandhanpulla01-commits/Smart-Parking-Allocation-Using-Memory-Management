#include <Servo.h>

// -------------------------
// PINS
// -------------------------
const int trigPin = 9;
const int echoPin = 10;

const int servoPin = 6;

const int greenLED = 7;
const int redLED = 8;

const int firstFitButton = A0;
const int bestFitButton = A1;
const int worstFitButton = A2;

const int detectionDistance = 20;

Servo gateServo;

bool vehiclePresent = false;
bool algorithmSelected = false;


// -------------------------
// DISTANCE
// -------------------------
float getDistance() {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);

  if (duration == 0)
    return 999;

  return duration * 0.0343 / 2;
}


// -------------------------
// SETUP
// -------------------------
void setup() {

  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  pinMode(firstFitButton, INPUT_PULLUP);
  pinMode(bestFitButton, INPUT_PULLUP);
  pinMode(worstFitButton, INPUT_PULLUP);

  gateServo.attach(servoPin);
  gateServo.write(0);

  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);

  Serial.println("SMART_PARKING_READY");
}


// -------------------------
// MAIN LOOP
// -------------------------
void loop() {

  // =================================
  // RECEIVE COMMAND FROM PYTHON
  // =================================

  if (Serial.available() > 0) {

    String command = Serial.readStringUntil('\n');
    command.trim();

    // Python says allocation succeeded
    if (command == "OPEN_GATE") {

      digitalWrite(redLED, LOW);
      digitalWrite(greenLED, HIGH);

      Serial.println("GATE_OPENING");

      gateServo.write(90);

      delay(3000);

      gateServo.write(0);

      Serial.println("GATE_CLOSED");

      delay(1000);

      digitalWrite(greenLED, LOW);
    }

    // Python says allocation failed
    else if (command == "ALLOCATION_FAILED") {

      digitalWrite(redLED, HIGH);

      Serial.println("ALLOCATION_FAILED");

      delay(2000);

      if (!vehiclePresent) {
        digitalWrite(redLED, LOW);
      }
    }
  }


  // =================================
  // VEHICLE DETECTION
  // =================================

  float distance = getDistance();

  if (distance <= detectionDistance && !vehiclePresent) {

    vehiclePresent = true;
    algorithmSelected = false;

    digitalWrite(redLED, HIGH);

    Serial.println("VEHICLE_DETECTED");
  }


  if (distance > detectionDistance && vehiclePresent) {

    vehiclePresent = false;
    algorithmSelected = false;

    digitalWrite(redLED, LOW);

    Serial.println("VEHICLE_LEFT");
  }


  // =================================
  // FIRST FIT BUTTON
  // =================================

  if (vehiclePresent &&
      !algorithmSelected &&
      digitalRead(firstFitButton) == LOW) {

    delay(150);

    if (digitalRead(firstFitButton) == LOW) {

      algorithmSelected = true;

      Serial.println("FIRST_FIT");

      while (digitalRead(firstFitButton) == LOW) {
        delay(10);
      }
    }
  }


  // =================================
  // BEST FIT BUTTON
  // =================================

  if (vehiclePresent &&
      !algorithmSelected &&
      digitalRead(bestFitButton) == LOW) {

    delay(150);

    if (digitalRead(bestFitButton) == LOW) {

      algorithmSelected = true;

      Serial.println("BEST_FIT");

      while (digitalRead(bestFitButton) == LOW) {
        delay(10);
      }
    }
  }


  // =================================
  // WORST FIT BUTTON
  // =================================

  if (vehiclePresent &&
      !algorithmSelected &&
      digitalRead(worstFitButton) == LOW) {

    delay(150);

    if (digitalRead(worstFitButton) == LOW) {

      algorithmSelected = true;

      Serial.println("WORST_FIT");

      while (digitalRead(worstFitButton) == LOW) {
        delay(10);
      }
    }
  }


  delay(100);
}