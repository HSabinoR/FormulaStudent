#include <mcp_can.h>
#include <SPI.h>

const int sensorPin = A1;
int old_value;
MCP_CAN mcp2515(10);    // CS pin connected to digital pin 10

void setup() {
  Serial.begin(9600);
  if(mcp2515.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.println("MCP2515 Initialized!!");
  } else{
    Serial.println("Error Intializing MCP2515!!");
    while(1);
  }
  mcp2515.setMode(MCP_NORMAL);
}

void loop() {
  // Double read
  int raw_Value = analogRead(sensorPin);
  //int raw_Value = analogRead(sensorPin);
/*
  raw_Value = constrain(5, 1023);
  if (raw_Value < (old_value - 2) || raw_Value > (old_value + 2)){
    old_value = raw_Value; // Change this to low pass filter
  }*/
  sendNumber(0x123, 0, 2, raw_Value);
}

void sendNumber(uint32_t id, int ext, int dlc, int sensorValue) {
  byte data[dlc] = {};

  //data[0] = sensorValue;
  // splits the 16 bit int number into two bytes
  data[0] = lowByte(sensorValue);
  data[1] = highByte(sensorValue);

  mcp2515.sendMsgBuf(id, ext, dlc, data);
}

