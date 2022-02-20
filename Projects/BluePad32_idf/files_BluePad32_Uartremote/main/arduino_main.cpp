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

#include "driver/i2s.h"


#include <Arduino.h>
#include <Wire.h>
#include <Bluepad32.h>
#include <UartRemote.h>
#include <Adafruit_NeoPixel.h>
#include <arduinoFFT.h>

const i2s_port_t I2S_PORT = I2S_NUM_0;

static GamepadPtr myGamepad;

UartRemote uartremote;

arduinoFFT FFT = arduinoFFT(); /* Create FFT object */
/*
These values can be changed in order to evaluate the functions
*/
const uint16_t samples = 64; //This value MUST ALWAYS be a power of 2
const double signalFrequency = 1000;
const double samplingFrequency = 5000;
const uint8_t amplitude = 100;
/*
These are the input and output vectors
Input vectors receive computed results from FFT
*/
double vReal[samples];
double vImag[samples];
int16_t rawsamples[samples];

float spectrum[5] = {};

Arguments args;

#define LED_PIN 21
#define LED_COUNT 64

// use pointer allows to dynamically change nrumber of leds or pin
// change strip.begin() to strip->begin(), etc.
// delete object before initiating a new one
Adafruit_NeoPixel* strip = new Adafruit_NeoPixel(LED_COUNT,LED_PIN); //, NEO_GRB + NEO_KHZ800);



// This callback gets called any time a new gamepad is connected.
// Up to 4 gamepads can be connected at the same time.
void onConnectedGamepad(GamepadPtr gp) {
    // In this example we only use one gamepad at the same time.
    myGamepad = gp;
    /*
    args=uartremote.call("connected","B",0);
    if (args.error==0) { // no error
            printf("received ack\n");
        } else { printf("error from call connected\n");}
    */
    Serial.println("CALLBACK: Gamepad is connected!");
}

void onDisconnectedGamepad(GamepadPtr gp) {
    Serial.println("CALLBACK: Gamepad is disconnected!");
    /*
    args=uartremote.call("disconnected","B",0);
    if (args.error==0) { // no error
            printf("received ack\n");
        } else { printf("error from call isconnected\n");}
    */
    myGamepad = nullptr;
}
uint8_t old_led=0,rumble_force,rumble_duration;

void connected(Arguments args) {
    if (myGamepad && myGamepad->isConnected()) {
        uartremote.send_command("connectedack","B",1);
    } else {
        uartremote.send_command("connectedack","B",0);
    }

}

void gamepad(Arguments args) {
    if (myGamepad && myGamepad->isConnected()) {
        uartremote.send_command("gamepadack","2H4h",myGamepad->buttons(),myGamepad->dpad(),
                                            myGamepad->axisX(),myGamepad->axisY(),
                                            myGamepad->axisRX(),myGamepad->axisRY());
    }
    else {
        uartremote.send_command("gamepadack","2H4h",0,0,0,0,0,0);
    }    
}

void led(Arguments args) {
    uint8_t led_value;
    unpack(args,&led_value);
    if (led_value!=old_led) {
        if (myGamepad && myGamepad->isConnected()) {
            myGamepad->setPlayerLEDs(led_value & 0x0f);
            old_led=led_value;
        }
    }
    Serial.printf("LED on: %d\n", led_value);
    uartremote.send_command("ledack","B",0);
}

void rumble(Arguments args) {
    unpack(args,&rumble_force,&rumble_duration);

    if ((rumble_force>0) && (rumble_duration>0)) {
        if (myGamepad && myGamepad->isConnected()) {
                myGamepad->setRumble(rumble_force /* force */, rumble_duration/* duration */);
        }
    }
    Serial.printf("rumble force %d, duration%d\n", rumble_force,rumble_duration);
    uartremote.send_command("rumbleack","B",0);
}

void servo(Arguments args) {
    /*
    call("servo","Bi",servo_nr,servo_pwm)
    */
    uint8_t servo_nr;
    uint32_t servo_pwm;
    unpack(args,&servo_nr,&servo_pwm);
    Serial.printf("servo_nr %d, pwm%d\n",servo_nr,servo_pwm);
    uartremote.send_command("servoack","B",0);
}

uint8_t scan_i2c(uint8_t addresses[]) {
    byte error, address; //variable for error and I2C address
    int nDevices=0;
    for (address = 1; address < 127; address++ )
    {
        // The i2c_scanner uses the return value of
        // the Write.endTransmisstion to see if
        // a device did acknowledge to the address.
        Wire.beginTransmission(address);
        error = Wire.endTransmission();

        if (error == 0)
        {
          addresses[nDevices]=address;
          nDevices++;
        }
        
    }
    
    return nDevices;
}

void i2c_scan(Arguments args) {
  uint8_t addresses[128],nDevices;
  nDevices=scan_i2c(addresses);  
  char format[7]={};
  sprintf(format,"B%ds",nDevices); // create variable format string
  uartremote.send_command("i2c_scan",format,nDevices,addresses);
}


void i2c_read(Arguments args) {
    /*
    call("i2c_read","2B",address,len)
    */
    uint8_t address,len;
    uint8_t buf[128];
    char format[7]={};
    unpack(args,&address,&len);
    Wire.requestFrom(address, len);    // request 6 bytes from slave device #2
    for (int i=0; i<len; i++) {
        char c = Wire.read();    // receive a byte as character
        buf[i]=c;
    }
   
    sprintf(format,"%ds",len); // create variable format string
    uartremote.send_command("i2c_readack",format,buf);
}

void i2c_read_reg(Arguments args) {
    /*
    call("i2c_read_reg","2B",address,reg,len)

    returns: bytes: buf
    */

    uint8_t address,len,reg;
    uint8_t buf[128];
    char format[7]={};
    unpack(args,&address,&reg,&len);

    Wire.beginTransmission(address);    // Get the slave's attention, tell it we're sending a command byte
    Wire.write(reg);                               //  The command byte, sets pointer to register with address of 0x32
    Wire.requestFrom(address,len);          // Tell slave we need to read 1byte from the current register
     for (int i=0; i<len; i++) {
        char c = Wire.read();    // receive a byte as character
        buf[i]=c;
    }
   
    Wire.endTransmission();       
   
    sprintf(format,"%ds",len); // create variable format string
    uartremote.send_command("i2c_read_regack",format,buf);
}

void neopixel(Arguments args) {
    /*
    call("neopixel","4B",nr,r,g,b) 
    */
   uint8_t led_nr,red,green,blue;
   unpack(args,&led_nr,&red,&green,&blue);
   strip->setPixelColor(led_nr, red, green, blue);
   uartremote.send_command("neopixelack","B",0);
}


void neopixel_init(Arguments args) {
    /*
    call("neopixel_init","2B",nr_leds,pin) 
    */
   uint8_t nr_leds,pin;
   unpack(args,&nr_leds,&pin);
   delete strip;
   strip=new Adafruit_NeoPixel(nr_leds,pin);
   uartremote.send_command("neopixel_initack","B",0);
}

void neopixel_show(Arguments args) {
    /*
    call("neopixel_show") 
    */
   strip->show();
   uartremote.send_command("neopixel_showack","B",0);
}

void fft(Arguments args){
    uartremote.send_command("fftack","5f",
              spectrum[0],spectrum[1],spectrum[2],spectrum[3],spectrum[4]);

}
// Arduino setup function. Runs in CPU 1
void setup() {
    Serial.begin(115200);
    Wire.begin(5,4); // sda=pin(5), scl=Pin(4)
    strip->begin();
    strip->show(); // Initialize all pixels to 'off'


    // add uartremote commands
    uartremote.add_command("connected",&connected);
    uartremote.add_command("gamepad",&gamepad);
    uartremote.add_command("led", &led);
    uartremote.add_command("rumble", &rumble);
    uartremote.add_command("servo", &servo);
    uartremote.add_command("i2c_scan", &i2c_scan);
    uartremote.add_command("i2c_read", &i2c_read);
    uartremote.add_command("i2c_read_reg", &i2c_read_reg);
    uartremote.add_command("neopixel",&neopixel);
    uartremote.add_command("neopixel_show",&neopixel_show);
    uartremote.add_command("neopixel_init",&neopixel_init);
    uartremote.add_command("fft",&fft);
    String fv = BP32.firmwareVersion();
    Serial.print("Firmware: ");
    Serial.println(fv);

    // Setup the Bluepad32 callbacks
    BP32.setup(&onConnectedGamepad, &onDisconnectedGamepad);


#define SAMPLE_RATE 5000

    // I2S
const i2s_config_t i2s_config = {
    .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX), // receive
    .sample_rate = SAMPLE_RATE,                        // 44100 (44,1KHz)
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT, // 32 bits per sample
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,  // use right channel
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1, // interrupt level 1
    .dma_buf_count = 64,                      // number of buffers
    .dma_buf_len = 512};       // 512

    // pin config
const i2s_pin_config_t pin_config = {
    .bck_io_num = 33,            // serial clock, sck (gpio 33)
    .ws_io_num = 27,              // word select, ws (gpio 32)
    .data_out_num = I2S_PIN_NO_CHANGE, // only used for speakers
    .data_in_num = 32             // serial data, sd (gpio 34)
    };

// config i2s driver and pins
// fct must be called before any read/write
esp_err_t err = i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
if (err != ESP_OK)
{
    Serial.printf("Failed installing the driver: %d\n", err);
}

err = i2s_set_pin(I2S_PORT, &pin_config);
if (err != ESP_OK)
{
    Serial.printf("Failed setting pin: %d\n", err);
}

Serial.println("I2S driver installed! :-)");

}

// Arduino loop function. Runs in CPU 1
void loop() {
    // This call fetches all the gamepad info from the NINA (ESP32) module.
    // Just call this function in your main loop.
    // The gamepads pointer (the ones received in the callbacks) gets updated
    // automatically.
    BP32.update();

    if (uartremote.available()>0) {
        int error = uartremote.receive_execute();
        if (error==1) {
            printf("error in receiving command\n");
        }
    }
    delay(10);

   
    // 64 samples @ 5000 Hz = 12.8ms chunks of samples --> FFT --> 32 frequency points

    size_t i2s_bytes_read;
    i2s_read(I2S_PORT, rawsamples, 64, &i2s_bytes_read, 100);
    int32_t blockSum = rawsamples[0];

    for (uint16_t i = 1; i < 64; i++)
    {
        blockSum += rawsamples[i];
    }

    // Compute average value for the current sample block
    int16_t blockAvg = blockSum / 64;
    // Constant for normalizing int16 input values to floating point range -1.0 to 1.0
    const float kInt16MaxInv = 1.0f / __INT16_MAX__;
    for (uint16_t i = 0; i < samples; i++)
    {
        vReal[i] = (rawsamples[i]-blockAvg)*kInt16MaxInv;/* Build data with positive and negative values*/
        vImag[i] = 0.0; //Imaginary part must be zeroed in case of looping to avoid wrong calculations and overflows
    }
    // FFT.DCRemoval(vReal, samples);
    FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);	/* Weigh data */
    FFT.Compute(vReal, vImag, samples, FFT_FORWARD); /* Compute FFT */
    FFT.ComplexToMagnitude(vReal, vImag, samples); /* Compute magnitudes */
    // make 5 bins of the power spectrum
    for (uint8_t i=0; i<5; i++) {
        double s=0;
        for (uint8_t j=0; j<6; j++ ) {
           s+=vReal[i*6+j+1]; // +1 skip dc compontent
        }
        spectrum[i]=s; // update spectrum array
    }
 
}
