#include <mcp_can.h>
#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>

long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[2];

#define CAN_INT 2 // Set INT to pin 2
MCP_CAN mcp2515(10); // Set CS to pin 10

#define CE_PIN 9
#define CSN_PIN 10

#define INTERVAL_MS_TRANSMISSION 2

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
  Serial.begin(115200);
  /// MCP2515 Intialization ///

  // Initialize MCP2515 running at 16MHz with a baudrate 500kb/s and the masks and filters disabled.
  if(mcp2515.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK){
    //Serial.println("MCP2515 Initialized Successfully!");
  }else {
    Serial.println("Error Initializing MCP2515...");
  }
  mcp2515.setMode(MCP_NORMAL);
  
  pinMode(CAN_INT, INPUT);
  

  /// NRF24L01 Intialization ///

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
  }else{
    Serial.println("No connection between nRF24L01 and Arduino! ");
  }
}

void loop() {
  if(!digitalRead(CAN_INT))                         // If CAN0_INT pin is low, read receive buffer
  {
    mcp2515.readMsgBuf(&rxId, &len, rxBuf);

    if(rxId == 0x123){
      payload.brake_power = receiveNumber(rxBuf);
    }else if(rxId == 0x456){
      //payload.throttle_power = receiveNumber(rxBuf);
      payload.throttle_power = 500;
    }else if(rxId == 0x789){
      //payload.brake_power = receiveNumber(rxBuf);
      payload.wheel_angle = 800;
    }    

    if(radio.write(&payload, sizeof(payload))) {
      Serial.print("Brake Power: ");
      Serial.print("Sent: (");
      Serial.print(payload.brake_power);
      Serial.print(" | Throttle Power: ");
      Serial.print(payload.throttle_power);
      Serial.print(" | Wheel Angle: ");
      Serial.print(payload.wheel_angle);
      Serial.println(")");
    }else {
      Serial.println("Error! Payload not sent");
    }
    delay(INTERVAL_MS_TRANSMISSION);
  }
}

int receiveNumber(byte *rxBuf) {
  int sensor_Value = (rxBuf[1] << 8) | rxBuf[0];
  return sensor_Value;
}
