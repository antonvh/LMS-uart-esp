# Combined firmware

## Prebuild firmware

The firmware in this directory can be flahed on the ESP32 using the folliwing command:

```
esptool.py --port /dev/ttyUSB0 --baud 500000 write_flash 0x1000  bluepad32_uartremote_firmware.bin
```

## Features

This is a firmware that supported BluePad32. Furthermore, the following commands are integrated in the firmware:

```
    uartremote.add_command("connected",&connected);
    uartremote.add_command("gamepad",&gamepad);
    uartremote.add_command("led", &led);
    uartremote.add_command("rumble", &rumble);
    uartremote.add_command("i2c_scan", &i2c_scan);
    uartremote.add_command("i2c_read", &i2c_read);
    uartremote.add_command("i2c_read_reg", &i2c_read_reg);
    uartremote.add_command("neopixel",&neopixel);
    uartremote.add_command("neopixel_show",&neopixel_show);
    uartremote.add_command("neopixel_init",&neopixel_init);
    uartremote.add_command("fft",&fft);
    uartremote.add_command("servo",&servo);
```

## Calling from Lego SPIKE Prime or Robot Invertor

**`ur.call('connected')`**

Check whether a gamepad is connected. Returns 1 when connected

**'ur.call('gamepad')`**

Returns the status of the gamepad with 6 parameters: `myGamepad->buttons(),myGamepad->dpad(),myGamepad->axisX(),myGamepad->axisY(),myGamepad->axisRX(),myGamepad->axisRY())`

**`ur.call('led','B',led_val)`**

Sets leds on gamepad to binary value `led_val`

**`ur.call('rumble',2B',force,duration)`**

Initiates rumble motor in gamepad with tyhe given force and duration.

**`ur.call('i2c_scan')`**

Returns the addresses of connected i2c devices. Note: returns a byte array.

**`ur.call('i2c_read',address,len)`**

Reads `len` bytes from i2c device (connected to the Grove port) at address `adress`

**`ur.call("neopixel","4B",led_nr,red,green,blue)`**

Sets led number `led_nr` to color `(red,greem,blue)`. Use led_show to display the leds.

**`ur.call('neopixel_show)`**

Shows current led configuration.

**`ur.call('neopixel_init','2B',number_leds,pin)`**

Initates NeoPixel with `number_leds` leds on Pin `pin`.

**`ur.call('fft')`**

Returns an array of 5 values containing the measured audio power in 5 frequency bands, each rougly 500Hz broad.

**`ur.call('servo','>Bi',servo_nr,pos)`**

Sets servo number `servo_nr` to position `pos`. Mapping is servo 1,2,3, and 4 on pins 21,22,23, and 25. Currently only servo1 supported.


