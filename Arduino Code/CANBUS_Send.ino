#include <mcp2515.h>
#include <SPI.h>
struct can_frame message;
const int potPin = A0;
MCP2515 mcp2515(10);    // CS pin connected to digital pin 10

void setup() {
  Serial.begin(9600);
  if(mcp2515.begin(MCP_ANY, CAN_100KBPS, MCP_8MHZ) == MCP2515::ERROR_OK) {
    Serial.println("MCP2515 Initialized!!");
  } else{
    Serial.println("Error Intializing MCP2515!!");
    while(1);
  }
}

void loop() {
  int raw_Value = analogRead(potPin);
  sendNumber(0x123, raw_Value);
}

void sendNumber(uint32_t id, int potValue) {
  message.can_id = id;
  message.can_dlc = 2;

  message.data[0] = lowByte(potValue);
  message.data[1] = highByte(potValue);

  message.sendMessage(&message);

}