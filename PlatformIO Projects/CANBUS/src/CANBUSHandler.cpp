#include "CANBUSHandler.h"
#include <SPI.h>

MCP_CAN CANBUSHandler::mcp2515(CAN_CS_PIN);

unsigned char CANBUSHandler::len = 0;

void CANBUSHandler::CANsetup(){
    Serial.begin(115200);
    /// MCP2515 Intialization ///

     // Initialize MCP2515 running at 16MHz with a baudrate 500kb/s and the masks and filters disabled.
    if(mcp2515.begin(MCP_ANY, can_DataRate, can_clock_speed) == CAN_OK){
        //Serial.println("MCP2515 Initialized Successfully!");
    }else {
        Serial.println("Error Initializing MCP2515...");
    }
    mcp2515.setMode(MCP_NORMAL);
  
    pinMode(CAN_INT, INPUT);
}

void CANBUSHandler::rxHandling(){
    if(!digitalRead(CAN_INT)){    // If CAN_INT pin is low, read receive buffer
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
    }
}

int receiveNumber(byte *rxBuf) {
    return (rxBuf[1] << 8) | rxBuf[0];
}