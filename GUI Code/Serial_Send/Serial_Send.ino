//const int brakesPin;
//const int throttlePin;
//const int wheelPin;

void setup() {
    Serial.begin(115200);
}

void loop() {
    //int brake_power = analogRead(brakesPin);
    //int throttle_power = analogRead(throttlePin);
    //int wheel_angle = analogRead(wheelPin);

    int brake_power = random(0,1023);
    int throttle_power = random(0,1023);
    int wheel_angle = random(0,1023);

    Serial.print(brake_power);
    Serial.print(",");
    Serial.print(throttle_power);
    Serial.print(",");
    Serial.print(wheel_angle);
    Serial.print('\n');
}
