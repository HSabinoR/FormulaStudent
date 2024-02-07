#include <Arduino.h>
#include "CANBUSHandler.h"
#include "Nrf24Handler.h"

void setup() {
    CANBUSHandler::CANsetup();
    nRF24Handler::rf24setup();
}

void loop() {
    CANBUSHandler::rxHandling();
    nRF24Handler::txHandling();
}