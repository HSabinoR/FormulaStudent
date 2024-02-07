#ifndef CANBUSHandler_h
#define CANBUSHandler_h

#include <mcp_can.h>
#include <config.h>

class CANBUSHandler{
    public:
            static void CANsetup();
            static void rxHandling();
            static long unsigned int rxId;
            static unsigned char len;
            static unsigned char rxBuf[2];
    
    private:
            static MCP_CAN mcp2515;
};

#endif