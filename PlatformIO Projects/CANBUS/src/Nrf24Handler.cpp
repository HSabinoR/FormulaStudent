#include "Nrf24Handler.h"
#include <SPI.h>

RF24 nRF24Handler::radio(rf24_CE_PIN, rf24_CS_PIN);

void nRF24Handler::rf24setup(){
    if (radio.isChipConnected()) {
    //Serial.println("nRF24L01 Intialiazed!");
    
    //Append ACK packet from the receiving radio back to the transmitting radio
    radio.setAutoAck(false); //(true|false)

    //Set the transmission datarate
    radio.setDataRate(nRF24_DataRate); //(RF24_250KBPS|RF24_1MBPS|RF24_2MBPS)

    radio.setPALevel(nRF24_PALevel); //(RF24_PA_MIN|RF24_PA_LOW|RF24_PA_HIGH|RF24_PA_MAX)

    //Default value is the maximum 32 bytes
    radio.setPayloadSize(6);

    radio.openWritingPipe(NRF24_ADDRESS);
    radio.stopListening();
    }else{
        Serial.println("No connection between nRF24L01 and Arduino! ");
  }
}

void nRF24Handler::txHandling(){
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