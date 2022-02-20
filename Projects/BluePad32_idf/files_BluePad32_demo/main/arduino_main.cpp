/****************************************************************************
http://retro.moe/unijoysticle2

Copyright 2021 Ricardo Quesada

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
****************************************************************************/

#include "sdkconfig.h"
#ifndef CONFIG_BLUEPAD32_PLATFORM_ARDUINO
#error "Must only be compiled when using Bluepad32 Arduino platform"
#endif // !CONFIG_BLUEPAD32_PLATFORM_ARDUINO

#include <Arduino.h>
#include <Bluepad32.h>
#include <UartRemote.h>

static GamepadPtr myGamepad;

UartRemote uartremote;

Arguments args;


// This callback gets called any time a new gamepad is connected.
// Up to 4 gamepads can be connected at the same time.
void onConnectedGamepad(GamepadPtr gp) {
    // In this example we only use one gamepad at the same time.
    myGamepad = gp;
    args=uartremote.call("connected","B",0);
    if (args.error==0) { // no error
            printf("received ack\n");
        } else { printf("error from call connected\n");}

    Serial.println("CALLBACK: Gamepad is connected!");
}

void onDisconnectedGamepad(GamepadPtr gp) {
    Serial.println("CALLBACK: Gamepad is disconnected!");
    args=uartremote.call("disconnected","B",0);
    if (args.error==0) { // no error
            printf("received ack\n");
        } else { printf("error from call isconnected\n");}
    myGamepad = nullptr;
}

// Arduino setup function. Runs in CPU 1
void setup() {
    Serial.begin(115200);

    String fv = BP32.firmwareVersion();
    Serial.print("Firmware: ");
    Serial.println(fv);

    // Setup the Bluepad32 callbacks
    BP32.setup(&onConnectedGamepad, &onDisconnectedGamepad);
}

uint8_t old_led=0,led,rumble_force,rumble_duration;
// Arduino loop function. Runs in CPU 1
void loop() {
    // This call fetches all the gamepad info from the NINA (ESP32) module.
    // Just call this function in your main loop.
    // The gamepads pointer (the ones received in the callbacks) gets updated
    // automatically.
    BP32.update();

    // It is safe to always do this before using the gamepad API.
    // This guarantees that the gamepad is valid and connected.
    if (myGamepad && myGamepad->isConnected()) {
        // There are different ways to query whether a button is pressed.
        // By query each button individually:
        //  a(), b(), x(), y(), l1(), etc...
        
        if (myGamepad->b()) {
            // Turn on the 4 LED. Each bit represents one LED.
            static int led = 0;
            led++;
            // Some gamepads like the DS3, DualSense, Nintendo Wii, Nintendo Switch
            // support changing the "Player LEDs": those 4 LEDs that usually indicate
            // the "gamepad seat".
            // It is possible to change them by calling:
            myGamepad->setPlayerLEDs(led & 0x0f);
        }

        if (myGamepad->x()) {
            // Duration: 255 is ~2 seconds
            // force: intensity
            // Some gamepads like DS3, DS4, DualSense, Switch, Xbox One S support
            // rumble.
            // It is possible to set it by calling:
            myGamepad->setRumble(0xc0 /* force */, 0xc0 /* duration */);
        }

        // Another way to query the buttons, is by calling buttons(), or
        // miscButtons() which return a bitmask.
        // Some gamepads also have DPAD, axis and more.
        
        args=uartremote.call("gamepad","2H4h",myGamepad->buttons(),myGamepad->dpad(),
                                            myGamepad->axisX(),myGamepad->axisY(),
                                            myGamepad->axisRX(),myGamepad->axisRY());
        
        if (args.error==0) { // no error

            unpack(args,&led,&rumble_force,&rumble_duration);
            if (led!=old_led) {
                myGamepad->setPlayerLEDs(led & 0x0f);
                old_led=led;
            }
            if ((rumble_force>0) && (rumble_duration>0)) {
                myGamepad->setRumble(rumble_force /* force */, rumble_duration/* duration */);
            }
            
        } else { printf("error from call gamepad\n");}

        

    }
    delay(10);
}
