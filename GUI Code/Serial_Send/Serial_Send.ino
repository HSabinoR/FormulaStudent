//const int sensorPin;
void setup() {
    Serial.begin(115200);
}

void loop() {
    //int sensorValue = analogRead(sensorPin);
    int testV1 = random(0,1023);
    int testV2 = random(0,1023);

    Serial.print(testV1);
    Serial.print(",");
    Serial.print(testV2);
    Serial.print('\n');
    delay(20);
}
