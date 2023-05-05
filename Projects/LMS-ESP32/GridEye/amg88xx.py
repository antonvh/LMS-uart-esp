# The MIT License (MIT)
#
# Copyright (c) 2017 Dean Miller for Adafruit Industries.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Original author(s): Dean Miller, Scott Shawcroft for Adafruit Industries.
# Date: June 2017
# Affiliation: Adafruit Industries
# Ported to MicroPython and extended by Peter Hinch
# This port copyright (c) Peter Hinch 2019

from micropython import const


# Possible register values.

# Operating Modes
_NORMAL_MODE = const(0x00)
_SLEEP_MODE = const(0x10)  # error in original
_STAND_BY_60 = const(0x20)
_STAND_BY_10 = const(0x21)

# sw resets
_FLAG_RESET = const(0x30)
_INITIAL_RESET = const(0x3F)

# frame rates
_FPS_10 = const(0x00)
_FPS_1 = const(0x01)

# int enables
_INT_DISABLED = const(0x00)
_INT_ENABLED = const(0x01)

# int modes
_DIFFERENCE = const(0x00)
_ABSOLUTE_VALUE = const(0x01)

_INT_OFFSET = const(0x010)
_PIXEL_OFFSET = const(0x80)

_PIXEL_ARRAY_WIDTH = const(8)
_PIXEL_ARRAY_HEIGHT = const(8)
_PIXEL_TEMP_CONVERSION = .25
_THERMISTOR_CONVERSION = .0625

# Registers
_PCTL = const(0)
_RST = const(1)
_FPS = const(2)
_INTEN = const(3)
_TTHL = const(0x0e)
_TTHH = const(0x0f)
_MAMOD = const(0x07)
_MAMOD1 = const(0x15)


class AMG88XX:

    @staticmethod
    def _validrc(row, col):
        if min(row, col) >= 0 and row < _PIXEL_ARRAY_HEIGHT and col < _PIXEL_ARRAY_WIDTH:
            return
        raise ValueError('Invalid row {} or col {}'.format(row, col))

    def __init__(self, i2c, addr=0x69):
        if addr not in i2c.scan():
            raise RuntimeError('AMG8833 not found at address 0x{:02x}'.format(addr))
        self._i2c = i2c
        self._address = addr
        self._scale = 2
        self._mamod = False
        # Pixel buffer 2 bytes/pixel (128 bytes)
        self._buf = bytearray(_PIXEL_ARRAY_HEIGHT * _PIXEL_ARRAY_WIDTH * 2)
        self._buf2 = bytearray(2)

        # enter normal mode
        self._write(_PCTL, _NORMAL_MODE)

        # software reset
        self._write(_RST, _INITIAL_RESET)

        # disable interrupts by default
        self._write(_INTEN, 0)

        # set to 10 FPS
        self._write(_FPS, _FPS_10)

    # read byte from register, return int
    def _read(self, memaddr, buf=bytearray(1)):  # memaddr = memory location within the I2C device
        self._i2c.readfrom_mem_into(self._address, memaddr, buf)
        return buf[0]

    # write byte to register
    def _write(self, memaddr, data, buf=bytearray(1)):
        buf[0] = data
        self._i2c.writeto_mem(self._address, memaddr, buf)

    # read n bytes, return buffer
    def _readn(self, buf, memaddr):  # memaddr = memory location within the I2C device
        self._i2c.readfrom_mem_into(self._address, memaddr, buf)
        return buf

    # Sensor temperature in Celcius
    def temperature(self):
        self._readn(self._buf2, _TTHL)
        v = ((self._buf2[1] << 8) | self._buf2[0]) & 0xfff
        if v & 0x800:
            v = -(v & 0x7ff)
        return float(v) * _THERMISTOR_CONVERSION

    # Set resolution: integer temps are shifted right 2 for °C
    def hi_res(self, v=None):
        if v is not None:
            self._scale = 0 if v else 2
        return self._scale == 0

    # Set or clear moving average mode
    def ma_mode(self, v=None):
        if v is not None:
            self._mamod = bool(v)  # Exception if illegal type passed
            v = 0x20 if v else 0
            self._write(_MAMOD1, 0x50)
            self._write(_MAMOD1, 0x45)
            self._write(_MAMOD1, 0x57)
            self._write(_MAMOD, v)
            self._write(_MAMOD1, 0)
        return self._mamod

    # Pixel temperature as integer Celcius. Access as sensor_instance[row, col]
    def __getitem__(self, index):
        row, col = index
        self._validrc(row, col)
        buf_idx = (row * _PIXEL_ARRAY_HEIGHT + col) * 2
        raw = ((self._buf[buf_idx + 1] << 8) | self._buf[buf_idx]) & 0xfff
        if raw & 0x800:
            raw -= 0x1000  # Sign extend
        return raw >> self._scale  # Pixel temp conversion == 0.25

    # Call before accessing a frame of data. Can be called in an ISR.
    # Blocks for 2.9ms on Pyboard 1.0
    def refresh(self, _=None):  # Dummy arg for use in timer callback
        i2c = self._i2c
        memaddr = _PIXEL_OFFSET
        i2c.readfrom_mem_into(self._address, memaddr, self._buf)