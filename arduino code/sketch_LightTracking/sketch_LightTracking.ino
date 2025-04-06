//#include <Stepper.h>
#include <AccelStepper.h>
const int stepsPerRevolution = 200; // number of steps in the stepper motor.
int data = 0;
int x = 0;
int y = 0;




const int dirPin1 = 6;
const int stepPin1 = 3;
const int dirPin2 = 5;
const int stepPin2 = 2;
int snapX = 0;
const int snapVal = 100;
const int snapSpeed = 5000;

// Define motor interface type
#define motorInterfaceType 1

// initialize the stepper library
AccelStepper myStepper1(motorInterfaceType, stepPin1, dirPin1);
AccelStepper myStepper2(motorInterfaceType, stepPin2, dirPin2);

//Stepper myStepper1(stepsPerRevolution, 9, 11, 10, 8);
//Stepper myStepper2(stepsPerRevolution, 5, 7, 6, 4);

void fastMove(AccelStepper myStepper, int snapVal, int snapSpeed){
    int oldSpeed = myStepper.speed();

    myStepper.setSpeed(snapSpeed);
    myStepper.move(snapVal);
    while (myStepper.runSpeedToPosition());

    myStepper.setSpeed(oldSpeed);
}

int makeSnapX(AccelStepper myStepper, int x) {
    // check if switching from -x to x or vice versa, fast move
    if (x == 0){ 
        return snapX;
    }

    switch (snapX) {
        case 1:
            if (x > 0) {
                return snapX;
            } else {
                fastMove(myStepper, snapVal, snapSpeed);
                return -1;
            }
            break;
        case -1:
            if (x < 0) {
                return snapX;
            } else {
                fastMove(myStepper, -snapVal, snapSpeed);
                return 1;
            }
            break;
        case 0:
            if (x > 0) {
                return 1;
            }
            else{
                return -1;
            }
    }
}

void setup() {
    Serial.begin(38400); // Start serial communication
    while (!Serial) {}  // Wait for serial connection (only necessary for some boards)
    pinMode(6, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(2, OUTPUT);

    // set speed of motors.
    //myStepper1.setSpeed(300);
    //myStepper2.setSpeed(300);
    myStepper1.setMaxSpeed(500);
    myStepper1.setAcceleration(200);
    myStepper1.setSpeed(500);
    myStepper1.move(0);

    myStepper2.setMaxSpeed(500);
    myStepper2.setAcceleration(200);
    myStepper2.setSpeed(500);
    myStepper2.move(0);
}

void loop() {
    if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');  // Read incoming data until newline
        int commaIndex = data.indexOf(',');
        
        if (commaIndex > 0) {  // Ensure valid data
            int x = data.substring(0, commaIndex).toInt();
            int y = data.substring(commaIndex + 1).toInt();

            // set the speeds to the values send from serial. Map the speeds and make sure they are positive.
            x = map(x, -1500, 1500, -30, 30);
            //speedX = abs(speedX);
            y = map(y, -1000, 1000, -10, 10);
            //speedY = abs(speedY);

            // actually set the speeds.
            //yStepper1.setSpeed(speedX);
            //myStepper2.setSpeed(-speedY);

            // set where to move the thing.
            snapX = makeSnapX(myStepper1, x);
            myStepper1.move(x);
            myStepper2.move(-y);

            // confirm coordinates on serial.
            Serial.print("Received X: ");
            Serial.print(x);
            Serial.print(", Y: ");
            Serial.println(y);

        }
    }

    // move stepper motor in the positive or negative direction
    myStepper1.run();
    myStepper2.run();
}

