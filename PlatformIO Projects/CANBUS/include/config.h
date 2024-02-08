#ifndef config_h
#define config_h

#define debuggingMode False;

struct Payload {
    static int brake_power;
    static int throttle_power;
    static int wheel_angle;
};
static Payload payload;

// Pin configurations
#define CAN_INT 2
#define CAN_CS_PIN 10
#define rf24_CE_PIN 6
#define rf24_CS_PIN 5

// Other configuration parameters

// CANBUS Config
#define can_DataRate CAN_500KBPS
/// Data Rate Speeds ///
//    CAN_4K096BPS    //
//    CAN_5KBPS       //
//    CAN_10KBPS      //
//    CAN_20KBPS      //
//    CAN_31K25BPS    //
//    CAN_40KBPS      //
//    CAN_50KBPS      //
//    CAN_80KBPS      //
//    CAN_100KBPS     //
//    CAN_125KBPS     //
//    CAN_200KBPS     //
//    CAN_250KBPS     //
//    CAN_500KBPS     //
//    CAN_1000KBPS    //
#define can_clock_speed MCP_8MHZ // (MCP_8MHZ|MCP_16MHZ|MCP_20MHZ)

// nRF24 Config
#define nRF24_DataRate RF24_2MBPS // (RF24_250KBPS|RF24_1MBPS|RF24_2MBPS)
#define nRF24_PALevel RF24_PA_MIN // (RF24_PA_MIN|RF24_PA_LOW|RF24_PA_HIGH|RF24_PA_MAX)
#define INTERVAL_MS_TRANSMISSION 2
#define NRF24_ADDRESS 0xCC // nRf24 pipe address

#endif