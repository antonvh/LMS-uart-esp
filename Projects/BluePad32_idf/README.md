# BluePad32 for Lego robot

## installation

Install esp-idf as described here https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/#get-started-get-esp-idf

## Set-up BluePad32 idf Arduino environment

Full explanation is in: https://github.com/ricardoquesada/bluepad32/blob/main/docs/plat_arduino.md

Choose: option A

```
source esp-idf/export.sh
cd LMS-uart-esp/Projects/BluePad32_idf
git clone --recursive https://gitlab.com/ricardoquesada/esp-idf-arduino-bluepad32-template.git BluePad32_Uartremote
```
Build BluePad32 original app in BluePad32_Uartremote directory:

```
cd BluePad32_uartremote
idf.py build
```

Then integrate UartRemote library by doig the following:

in  `LMS-uart-esp/Projects/BluePad32_idf` do

```
cp -a main BLuePad32_Uartremote
cp -a components BLuePad32_Uartremote
cd BluePad32_uartremote
idf.py build
idf.py -p /dev/ttyUSB0 flash
idf.py -p /dev/ttyUSB0 monitor
```

## On Lego Spike Prime or Robot Inventor

Use Python code in `LMS-uart-esp/Projects/BluePad32_idf/SPIKE/bluepad32.py`

## changes to original project

Changes thay I have made:

* copied UartRemote (arduino) library in omponents/arduino/libraries
* in components/arduino/CMakeLists.txt make the following changes

under the line

```
set(LIBRARY_SRCS
```

add:

```
  libraries/UartRemote/src/UartRemote.cpp
  libraries/UartRemote/src/struct.c
  libraries/UartRemote/src/struct_endian.c

```

under

```
set(includedirs
  variants/${IDF_TARGET}/
  cores/esp32/
```

add:

```
libraries/UartRemote/src
```
