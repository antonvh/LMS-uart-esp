
from uartremote import *

machine.freq(160000000)


def bit24_to_bit16(colour):
    return  (colour[2] & 0xf8) << 8 | (colour[1] & 0xfc) << 3 | colour[0] >> 3      


class LCD:

u=UartRemote(port.A)
