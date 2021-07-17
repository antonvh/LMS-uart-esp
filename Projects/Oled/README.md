# OLED project

## hardware

We use an ssd1306 based OLED screen with an I2C interface. Connect the OLED screen with its I2C SDA pin the ESP8266 modules SDA pin, and its I2C SCL pin to the SCL pin of the ESP8266 module.

## Demonstration

### loading demo

Load the file `oled_ESP.py` via the WebREPL to the ESP8266. Then, paste the code of `oled_SPIKE.py` in an empty python project in the Lego Education SPIKE Prime IDE. Run the code on the SPIKE, and a scrolling text should be displayed.

### Video

Look in this [tutorial for background on tge UartRemote library](https://www.youtube.com/watch?v=3U67RWEsXiU) and for a [demo of the OLED screen](https://www.youtube.com/watch?v=3U67RWEsXiU&t=1962s).
Note that some of the commands in the UartRemote library are changed, since the video was recorded. 
