#ifndef Nrf24Handler_h
#define Nrf24Handler_h

#include <config.h>
#include <RF24.h>
#include <nRF24L01.h>
#include <printf.h>

class nRF24Handler{
    public:
            static void rf24setup();
            static void txHandling();
    
    private:
            static RF24 radio;
};

#endif