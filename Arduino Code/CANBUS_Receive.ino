#include <mcp2515.h>
#include <SPI.h>

MCP2515 mcp2515(10);    // CS pin connected to digital pin 10

void setup() {
  Serial.begin(9600);
  if(mcp2515.begin(MCP_ANY, CAN_100KBS, MCP_8MHZ) == MCP2515::ERROR_OK) {
    Serial.println("MCP2515 Initialized!!");
  } else{
    Serial.println("Error Intializing MCP2515!!");
    while(1);
  }

  // Set the MCP2515 to listen to all messages
  mcp2515.setFilter(MCP2515::MASK0, MCP2515::FILTER0, 0x00000456); //potentiometer data
  mcp2515.setFilter(MCP2515::MASK1, MCP2515::FILTER1, 0x00000123);
  
}

void loop() {
  // Check if a CAN message is available
  if (mcp2515.readMessage(&message) == MCP2515::ERROR_OK) {
    // Print the received data to the serial port
    Serial.print("Received Message - ID: ");
    Serial.print(message.can_id, HEX);
    Serial.print(", DLC: ");
    Serial.print(message.can_dlc);
    Serial.print(", Data: ");
    
    for (int i = 0; i < message.can_dlc; ++i) {
      Serial.print(message.data[i], HEX);
      Serial.print(" ");
    }
    
    Serial.println();
  }
  
  delay(1000);  // Wait for a second before checking for the next message
}