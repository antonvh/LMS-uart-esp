'''
LEGO SPIKE Prime Microbit Backpack
LPF2forMicrobit class allows communication between LEGO SPIKE Prime and Microbit Backpacks
Version Date: 01/08/2020

Tufts Center for Engineering Education and Outreach
Updated on: 01/08/2020
'''
import utime
import gc
from machine import UART,Pin
import machine

txpin=1
rxpin=3

uart=UART(0)

class LPF2:
     def __init__(self):
          self.connected = False
          self.tx = machine.Pin(txpin, machine.Pin.OUT)
          self.rx = machine.Pin(rxpin, machine.Pin.IN)
          

     def send_value(self, data):
          value = (data & 0xFF)
          payload = bytes([0xC0, value, 0xFF ^ 0xC0 ^ value])
          size = uart.write(payload)
          if not size:
               self.connected = False

     def initialize(self):
          
          self.tx.value(0)
          utime.sleep_ms(500)
          self.tx.value(1)
          uart.init(baudrate=2400, bits=8, parity=None, stop=1)
          uart.write(b'\x00')
          #uart.write(b'\x40\x23\x9C')  #CMD_TYPE (x40)  Type   checksum
          uart.write(b'\x40\x3e\x81')  #CMD_TYPE (x40)  Type   checksum
          uart.write(b'\x49\x00\x00\xB6')  #CMD_MODE (x49)  # Modes  # Views   checksum
          uart.write(b'\x52\x00\xC2\x01\x00\x6E')  #CMD_SPEED (x52)  baud (LSB first)   checksum
          uart.write(b'\x5F\x00\x00\x00\x02\x00\x00\x00\x02\xA0')  #CMD_VERSION (x5F)  Hardware_V  Software_V   checksum
          uart.write(b'\xA0\x00\x4C\x50\x46\x32\x2D\x44\x45\x54\x45\x43\x54\x00\x00\x00\x00\x00\x1D')  #CMD_INFO|bytes|mode  0 name 0   checksum
          uart.write(b'\x98\x01\x00\x00\x00\x00\x00\x00\x20\x41\x07')  #CMD_INFO|3|mode  1 (raw) raw_min  raw_max   checksum
          uart.write(b'\x98\x02\x00\x00\x00\x00\x00\x00\xC8\x42\xEF')  #CMD_INFO|3|mode  2 (pct) pct_min  pct_max   checksum
          uart.write(b'\x98\x03\x00\x00\x00\x00\x00\x00\x20\x41\x05')  #CMD_INFO|3|mode  3 (SI) si_min  si_max   checksum
          uart.write(b'\x80\x04\x00\x7B')  #CMD_INFO|size|mode  0,4,symbol   checksum
          uart.write(b'\x88\x05\x10\x00\x62')  #CMD_INFO|1|mode  5 (FM) Function Map-In   -out   checksum
          uart.write(b'\x90\x80\x01\x00\x03\x00\xED')  #CMD_INFO|2|mode  x80 sample_size   Data_type   Figures   Decimals   checksum
          utime.sleep_ms(5)
          uart.write(b'\x04')
          #display.show(4)
          starttime = utime.ticks_ms()
          currenttime = starttime
          while (currenttime-starttime) < 2000:
               utime.sleep_ms(5)
               data = uart.read(uart.any())
               if data.find(b'\x04') >= 0:
                    self.connected = True
                    #display.show(5)
                    currenttime = starttime+3000
               else:
                    self.connected = True
                    currenttime = utime.ticks_ms()
          self.tx.value(0)
          utime.sleep_ms(10)
          uart.init(baudrate=115200, bits=8, parity=None, stop=1)
          self.send_value(2)# Write your code here :-)