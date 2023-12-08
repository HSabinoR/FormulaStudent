#include <mcp_can.h>
#include <SPI.h>

const int sensorPin = A0;

MCP_CAN mcp2515(10);    // CS pin connected to digital pin 10

void setup() {
  Serial.begin(9600);
  if(mcp2515.begin(MCP_ANY, CAN_100KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.println("MCP2515 Initialized!!");
  } else{
    Serial.println("Error Intializing MCP2515!!");
    while(1);
  }
  mcp2515.setMode(MCP_NORMAL);
}

void loop() {
  int raw_Value = analogRead(sensorPin);
  sendNumber(0x123, 0, 2, raw_Value);
}

void sendNumber(uint32_t id, int ext, int dlc, int sensorValue) {
  byte data[dlc] = {};

  data[0] = lowByte(sensorValue);
  data[1] = highByte(sensorValue);

  mcp2515.sendMsgBuf(id, std, dlc, data);
}
// change