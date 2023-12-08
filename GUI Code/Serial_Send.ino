const int sensorPin;
void setup() {
    Serial.begin(9600);
}

void loop() {
    int sensorValue = analogRead(sensorPin);
    int testValue = 25;

    sensorValue = map(sensorValue, 0, 1023, -180, 180);

    Serial.print(sensorValue);
    Serial.print(",");
    Serial.println(testValue);
    delay(50);
}