# Try to drive Neopixel/ws2812 from the MINDSTORMS Robot Inventor Hub
# Using the SPI class from machin
# THIS DIDN'T WORK.



"""
`neopixel_spi`
================================================================================
SPI driven CircuitPython driver for NeoPixels.
* Author(s): Carter Nelson
"""

# Pixel color order constants
RGB = "RGB"
"""Red Green Blue"""
GRB = "GRB"
"""Green Red Blue"""
RGBW = "RGBW"
"""Red Green Blue White"""
GRBW = "GRBW"
"""Green Red Blue White"""

# SPDX-FileCopyrightText: 2019-2020 Roy Hooper
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pypixelbuf` - A pure python implementation of _pixelbuf
=================================================================
This class is used when _pixelbuf is not available in CircuitPython.  It is based on the work
in neopixel.py and adafruit_dotstar.py.
* Author(s): Damien P. George &  Limor Fried & Scott Shawcroft & Roy Hooper
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Pypixelbuf.git"

DOTSTAR_LED_START_FULL_BRIGHT = 0xFF
DOTSTAR_LED_START = 0b11100000  # Three "1" bits, followed by 5 brightness bits
DOTSTAR_LED_BRIGHTNESS = 0b00011111


class PixelBuf:  # pylint: disable=too-many-instance-attributes
    """
    A sequence of RGB/RGBW pixels.
    This is the pure python implementation of CircuitPython's _pixelbuf.
    :param ~int n: Number of pixels
    :param ~str byteorder: Byte order string constant (also sets bpp)
    :param ~float brightness: Brightness (0 to 1.0, default 1.0)
    :param ~bool auto_write: Whether to automatically write pixels (Default False)
    :param bytes header: Sequence of bytes to always send before pixel values.
    :param bytes trailer: Sequence of bytes to always send after pixel values.
    """

    def __init__(  # pylint: disable=too-many-locals,too-many-arguments
        self,
        n,
        byteorder="BGR",
        brightness=1.0,
        auto_write=False,
        header=None,
        trailer=None,
    ):

        bpp, byteorder_tuple, has_white, dotstar_mode = self.parse_byteorder(byteorder)

        self.auto_write = False

        effective_bpp = 4 if dotstar_mode else bpp
        _bytes = effective_bpp * n
        buf = bytearray(_bytes)
        offset = 0

        if header is not None:
            if not isinstance(header, bytearray):
                raise TypeError("header must be a bytearray")
            buf = header + buf
            offset = len(header)

        if trailer is not None:
            if not isinstance(trailer, bytearray):
                raise TypeError("trailer must be a bytearray")
            buf += trailer

        self._pixels = n
        self._bytes = _bytes
        self._byteorder = byteorder_tuple
        self._byteorder_string = byteorder
        self._has_white = has_white
        self._bpp = bpp
        self._pre_brightness_buffer = None
        self._post_brightness_buffer = buf
        self._offset = offset
        self._dotstar_mode = dotstar_mode
        self._pixel_step = effective_bpp

        if dotstar_mode:
            self._byteorder_tuple = (
                byteorder_tuple[0] + 1,
                byteorder_tuple[1] + 1,
                byteorder_tuple[2] + 1,
                0,
            )
            # Initialize the buffer with the dotstar start bytes.
            for i in range(self._offset, self._bytes + self._offset, 4):
                self._post_brightness_buffer[i] = DOTSTAR_LED_START_FULL_BRIGHT

        self._brightness = 1.0
        self.brightness = brightness

        self.auto_write = auto_write

    @staticmethod
    def parse_byteorder(byteorder):
        """
        Parse a Byteorder string for validity and determine bpp, byte order, and
        dostar brightness bits.
        Byteorder strings may contain the following characters:
            R - Red
            G - Green
            B - Blue
            W - White
            P - PWM (PWM Duty cycle for pixel - dotstars 0 - 1.0)
        :param: ~str bpp: bpp string.
        :return: ~tuple: bpp, byteorder, has_white, dotstar_mode
        """
        bpp = len(byteorder)
        dotstar_mode = False
        has_white = False

        if byteorder.strip("RGBWP") != "":
            raise ValueError("Invalid Byteorder string")

        try:
            r = byteorder.index("R")
            g = byteorder.index("G")
            b = byteorder.index("B")
        except ValueError as exc:
            raise ValueError("Invalid Byteorder string") from exc
        if "W" in byteorder:
            w = byteorder.index("W")
            byteorder = (r, g, b, w)
            has_white = True
        elif "P" in byteorder:
            lum = byteorder.index("P")
            byteorder = (r, g, b, lum)
            dotstar_mode = True
        else:
            byteorder = (r, g, b)

        return bpp, byteorder, has_white, dotstar_mode

    @property
    def bpp(self):
        """
        The number of bytes per pixel in the buffer (read-only).
        """
        return self._bpp

    @property
    def brightness(self):
        """
        Float value between 0 and 1.  Output brightness.
        When brightness is less than 1.0, a second buffer will be used to store the color values
        before they are adjusted for brightness.
        """
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        value = min(max(value, 0.0), 1.0)
        change = value - self._brightness
        if -0.001 < change < 0.001:
            return

        self._brightness = value

        if self._pre_brightness_buffer is None:
            self._pre_brightness_buffer = bytearray(self._post_brightness_buffer)

        # Adjust brightness of existing pixels
        offset_check = self._offset % self._pixel_step
        for i in range(self._offset, self._bytes + self._offset):
            # Don't adjust per-pixel luminance bytes in dotstar mode
            if self._dotstar_mode and (i % 4 != offset_check):
                continue
            self._post_brightness_buffer[i] = int(
                self._pre_brightness_buffer[i] * self._brightness
            )

        if self.auto_write:
            self.show()

    @property
    def byteorder(self):
        """
        ByteOrder string for the buffer (read-only)
        """
        return self._byteorder_string

    def __len__(self):
        """
        Number of pixels.
        """
        return self._pixels

    def show(self):
        """
        Call the associated write function to display the pixels
        """
        return self._transmit(self._post_brightness_buffer)

    def fill(self, color):
        """
        Fills the given pixelbuf with the given color.
        :param pixelbuf: A pixel object.
        :param color: Color to set.
        """
        r, g, b, w = self._parse_color(color)
        for i in range(self._pixels):
            self._set_item(i, r, g, b, w)
        if self.auto_write:
            self.show()

    def _parse_color(self, value):
        r = 0
        g = 0
        b = 0
        w = 0
        if isinstance(value, int):
            r = value >> 16
            g = (value >> 8) & 0xFF
            b = value & 0xFF
            w = 0

            if self._dotstar_mode:
                w = 1.0
        else:
            if len(value) < 3 or len(value) > 4:
                raise ValueError(
                    "Expected tuple of length {}, got {}".format(self._bpp, len(value))
                )
            if len(value) == self._bpp:
                if self._bpp == 3:
                    r, g, b = value
                else:
                    r, g, b, w = value
            elif len(value) == 3:
                r, g, b = value
                if self._dotstar_mode:
                    w = 1.0

        if self._bpp == 4:
            if self._dotstar_mode:
                # LED startframe is three "1" bits, followed by 5 brightness bits
                # then 8 bits for each of R, G, and B. The order of those 3 are configurable and
                # vary based on hardware
                w = (int(w * 31) & 0b00011111) | DOTSTAR_LED_START
            elif (
                self._has_white
                and (isinstance(value, int) or len(value) == 3)
                and r == g
                and g == b
            ):
                # If all components are the same and we have a white pixel then use it
                # instead of the individual components when all 4 values aren't explicitly given.
                w = r
                r = 0
                g = 0
                b = 0

        return (r, g, b, w)

    def _set_item(
        self, index, r, g, b, w
    ):  # pylint: disable=too-many-locals,too-many-branches,too-many-arguments
        if index < 0:
            index += len(self)
        if index >= self._pixels or index < 0:
            raise IndexError
        offset = self._offset + (index * self._bpp)

        if self._pre_brightness_buffer is not None:
            if self._bpp == 4:
                self._pre_brightness_buffer[offset + self._byteorder[3]] = w
            self._pre_brightness_buffer[offset + self._byteorder[0]] = r
            self._pre_brightness_buffer[offset + self._byteorder[1]] = g
            self._pre_brightness_buffer[offset + self._byteorder[2]] = b

        if self._bpp == 4:
            # Only apply brightness if w is actually white (aka not DotStar.)
            if not self._dotstar_mode:
                w = int(w * self._brightness)
            self._post_brightness_buffer[offset + self._byteorder[3]] = w

        self._post_brightness_buffer[offset + self._byteorder[0]] = int(
            r * self._brightness
        )
        self._post_brightness_buffer[offset + self._byteorder[1]] = int(
            g * self._brightness
        )
        self._post_brightness_buffer[offset + self._byteorder[2]] = int(
            b * self._brightness
        )

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._pixels)
            for val_i, in_i in enumerate(range(start, stop, step)):
                r, g, b, w = self._parse_color(val[val_i])
                self._set_item(in_i, r, g, b, w)
        else:
            r, g, b, w = self._parse_color(val)
            self._set_item(index, r, g, b, w)

        if self.auto_write:
            self.show()

    def _getitem(self, index):
        start = self._offset + (index * self._bpp)
        buffer = (
            self._pre_brightness_buffer
            if self._pre_brightness_buffer is not None
            else self._post_brightness_buffer
        )
        value = [
            buffer[start + self._byteorder[0]],
            buffer[start + self._byteorder[1]],
            buffer[start + self._byteorder[2]],
        ]
        if self._has_white:
            value.append(buffer[start + self._byteorder[3]])
        elif self._dotstar_mode:
            value.append(
                (buffer[start + self._byteorder[3]] & DOTSTAR_LED_BRIGHTNESS) / 31.0
            )
        return value

    def __getitem__(self, index):
        if isinstance(index, slice):
            out = []
            for in_i in range(
                *index.indices(len(self._post_brightness_buffer) // self._bpp)
            ):
                out.append(self._getitem(in_i))
            return out
        if index < 0:
            index += len(self)
        if index >= self._pixels or index < 0:
            raise IndexError
        return self._getitem(index)

    def _transmit(self, buffer):
        raise NotImplementedError("Must be subclassed")

class NeoPixel_SPI(PixelBuf):
    """
    A sequence of neopixels.
    :param ~busio.SPI spi: The SPI bus to output neopixel data on.
    :param int n: The number of neopixels in the chain
    :param int bpp: Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
    :param float brightness: Brightness of the pixels between 0.0 and 1.0 where 1.0 is full
    brightness
    :param bool auto_write: True if the neopixels should immediately change when set. If False,
    ``show`` must be called explicitly.
    :param tuple pixel_order: Set the pixel color channel order. GRBW is set by default.
    :param int frequency: SPI bus frequency. For 800kHz NeoPixels, use 6400000 (default).
    For 400kHz, use 3200000.
    :param float reset_time: Reset low level time in seconds. Default is 80e-6.
    :param byte bit0: Bit pattern to set timing for a NeoPixel 0 bit.
    :param byte bit1: Bit pattern to set timing for a NeoPixel 1 bit.
    Example:
    .. code-block:: python
        import board
        import neopixel_spi
        pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), 10)
        pixels.fill(0xff0000)
    """

    def __init__(
        self,
        spi,
        n,
        *,
        bpp=3,
        brightness=1.0,
        auto_write=True,
        pixel_order=None,
        frequency=6400000,
        reset_time=80e-6,
        bit0=0b11000000,
        bit1=0b11110000
    ):

        # configure bpp and pixel_order
        if not pixel_order:
            pixel_order = GRB if bpp == 3 else GRBW
        else:
            bpp = len(pixel_order)
            if isinstance(pixel_order, tuple):
                order_list = [RGBW[order] for order in pixel_order]
                pixel_order = "".join(order_list)

        # neopixel stuff
        self._bit0 = bit0
        self._bit1 = bit1
        self._trst = reset_time

        # set up SPI related stuff
        self._spi = spi
        self._spi.init(baudrate=frequency)
        # with self._spi as spibus:
        #     try:
        #         # get actual SPI frequency
        #         freq = spibus.frequency
        #     except AttributeError:
        #         # use nominal
        freq = frequency
        self._reset = bytes([0] * round(freq * self._trst / 8))
        self._spibuf = bytearray(8 * n * bpp)

        # everything else taken care of by base class
        super().__init__(
            n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
        )

    def deinit(self):
        """Blank out the NeoPixels."""
        self.fill(0)
        self.show()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    @property
    def n(self):
        """
        The number of neopixels in the chain (read-only)
        """
        return len(self)

    def _transmit(self, buffer):
        """Shows the new colors on the pixels themselves if they haven't already
        been autowritten."""
        self._transmogrify(buffer)
        # pylint: disable=no-member
        # with self._spi as spi:
            # write out special byte sequence surrounded by RESET
            # leading RESET needed for cases where MOSI rests HI
        self._spi.write(self._reset + self._spibuf + self._reset)

    def _transmogrify(self, buffer):
        """Turn every BIT of buf into a special BYTE pattern."""
        k = 0
        for byte in buffer:
            # MSB first
            for i in range(7, -1, -1):
                if byte >> i & 0x01:
                    self._spibuf[k] = self._bit1# A NeoPixel 1 bit
                else:
                    self._spibuf[k] = self._bit0# A NeoPixel 0 bit
                k += 1

from machine import Pin,SPI
spi = SPI(sck=Pin.board.PE15, mosi=Pin.board.PE2, miso=Pin.board.PE3)
npspi = NeoPixel_SPI(spi,8)
# This should fill our leds with a dim red. But they kept shining bright.
npspi.fill((100,0,0))
