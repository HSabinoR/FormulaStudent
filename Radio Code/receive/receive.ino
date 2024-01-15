#include "SPI.h"
#include "RF24.h"
#include "nRF24L01.h"

#define CE_PIN 9
#define CSN_PIN 10

#define INTERVAL_MS_SIGNAL_RETRY 2

RF24 radio(CE_PIN, CSN_PIN);

const uint8_t address = 0xCC;

//NRF24L01 buffer limit is 32 bytes (max struct size)
struct payload {
  int brake_power;
  int throttle_power;
  int wheel_angle;
};

payload payload;

void setup()
{
  Serial.begin(250000);
  radio.begin();
  
  if (radio.isChipConnected()) {
    
    //Serial.println("nRF24L01 Intialiazed!");
    
    //Append ACK packet from the receiving radio back to the transmitting radio
    radio.setAutoAck(false); //(true|false)

    //Set the transmission datarate
    radio.setDataRate(RF24_2MBPS); //(RF24_250KBPS|RF24_1MBPS|RF24_2MBPS)

    radio.setPALevel(RF24_PA_MIN);//(RF24_PA_MIN|RF24_PA_LOW|RF24_PA_HIGH|RF24_PA_MAX)

    //Default value is the maximum 32 bytes
    radio.setPayloadSize(6);

    radio.openReadingPipe(0, address);
    radio.startListening();
  }else{
    Serial.println("No connection between nRF24L01 and Arduino! ");
  }
}

void loop()
{
  if (radio.available()) {
    radio.read(&payload, sizeof(payload));
    /*
    Serial.print("Received: (");
    Serial.print("Brake Power: ");
    Serial.print(payload.brake_power);
    Serial.print(" | Throttle Power: ");
    Serial.print(payload.throttle_power);
    Serial.print(" | Wheel Angle: ");
    Serial.print(payload.wheel_angle);
    Serial.println(")");
    */
    Serial.print(payload.brake_power);
    Serial.print(",");
    Serial.print(payload.throttle_power);
    Serial.print(",");
    Serial.print(payload.wheel_angle);
    Serial.print('\n');
  }/*
  else{
    Serial.println("Nothing received!!");
    }*/
  delay(INTERVAL_MS_SIGNAL_RETRY);
}
