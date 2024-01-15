#include "SPI.h"
#include "RF24.h"
#include "nRF24L01.h"
#include <printf.h>

const int brakesPin = A0;
const int throttlePin = A2;
const int wheelPin = A3;


#define CE_PIN 9
#define CSN_PIN 10

#define INTERVAL_MS_TRANSMISSION 2

RF24 radio(CE_PIN, CSN_PIN);

//const byte address[6] = "00001";
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
  printf_begin();
  Serial.begin(9600);
  radio.begin();

  //Serial.println();
  //radio.printDetails();
  //Serial.println();

  
  if (radio.isChipConnected()) {
    //Serial.println("nRF24L01 Intialiazed!");
    
    //Append ACK packet from the receiving radio back to the transmitting radio
    radio.setAutoAck(false); //(true|false)

    //Set the transmission datarate
    radio.setDataRate(RF24_2MBPS); //(RF24_250KBPS|RF24_1MBPS|RF24_2MBPS)

    radio.setPALevel(RF24_PA_MIN); //(RF24_PA_MIN|RF24_PA_LOW|RF24_PA_HIGH|RF24_PA_MAX)

    //Default value is the maximum 32 bytes
    radio.setPayloadSize(6);

    radio.openWritingPipe(address);
    radio.stopListening();
    
    Serial.println();
    radio.printDetails();
    Serial.println();
  }else{
    Serial.println("No connection between nRF24L01 and Arduino! ");
  }
}

void loop()
{
  payload.brake_power = analogRead(brakesPin);
  payload.throttle_power = analogRead(throttlePin);
  payload.wheel_angle = analogRead(wheelPin);

  if(radio.write(&payload, sizeof(payload))) {
    /*Serial.print("Brake Power: ");
    Serial.print("Sent: (");
    Serial.print(payload.brake_power);
    Serial.print(" | Throttle Power: ");
    Serial.print(payload.throttle_power);
    Serial.print(" | Wheel Angle: ");
    Serial.print(payload.wheel_angle);
    Serial.println(")");
    */
    
  }else {
    Serial.println("Error! Payload not sent");
  }

  delay(INTERVAL_MS_TRANSMISSION);
}
