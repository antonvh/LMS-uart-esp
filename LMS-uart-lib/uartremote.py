"""
from uartremote import *

def led(v):
    print('led')
    for i in v:
        print(i)
    return 'ok'


def neo(v):
    print(v)
    n=v['n']
    pixels=v['p']
    np = neopixel.NeoPixel(machine.Pin(4), n)
    for i,pixel in enumerate(pixels):
        print(i,pixel)
        r,g,b=pixel
        np[i]=(r,g,b)
    np.write()

def imu():
    return([12.3,11.1,180.0])

def grideye(addr):
    a=[20,21,22,23,24,25,26,27,28]
    return a[addr%9]


def mag():
    x, y, z = mag_sensor.read()                                                                 
    return [x,y,z]   

# disable repl on uart
uos.dupterm(None, 1)


u=UartRemote(0)
u.add_command('grideye',grideye)
u.add_command('led',led)
from compas import *
mag_sensor = HMC5883L(scl=5,sda=4) 
u.add_command('mag',mag)

"""



"""
UartRemote class helps to send and receive commands together with accompanying data structures between two MicroPython instances using a UART connection.

The information is packetized using the follwowinf format

LL<json string>

where
LL = length of the total message encoded in a LSB word (2 Bytes)
<json string> a structure of the from {'c':<command>,'v':<value>} represented as a json stringg with
<command> a string indictating the remote command
<value> a python data structure (supported: dictionary, array, string, int, float)

The receive buffers of typical MicroPython UART implemenations are rather limited. Consequently,
the message structure should be kept small (typically <100Bytes)

Platforms supported are. Platform definition between brackets:

Lego EV3 (EV3)                  
ESP8266 (ESP8266)
OpenMV_H7 (H7)

Still to implement:
Spike Prime (SPIKE)
Lego Robot Inventor (INVENTOR)

"""


# check platform

PLATFORM="EV3"
try:
    from pybricks.iodevices import UARTDevice
except:
    PLATFORM="ESP8266"

# check OpenMV H7 platform
try:
    import omv
    PLATFORM="H7"
except:
    pass

import json
import struct

if PLATFORM=="ESP8266":
    from machine import UART
    from machine import Pin,I2C
    from compas import *
    import uos
elif PLATFORM=="EV3":
    from pybricks.iodevices import UARTDevice
    from pybricks.parameters import Port
elif PLATFORM=="H7":
    from pyb import UART



class UartRemote:
    commands={}

    def __init__(self,port,baudrate=115200,timeout=1000,debug=False):
        if PLATFORM=="EV3":
            self.uart = UARTDevice(port,baudrate=baudrate,timeout=timeout)
        elif PLATFORM=="H7":
            self.uart = UART(3, baudrate, timeout_char=timeout)                         # P4,P5 default uart
        elif PLATFORM=="ESP8266":    
            self.uart = UART(port,baudrate=baudrate,timeout=timeout,rxbuf=100)
        else:
            raise RuntimeError('MicroPython Platform not defined')
        self.DEBUG=debug

    def add_command(self,command,command_function):
        self.commands[command]=command_function

    def debug(self,s):
        if self.DEBUG:
            print(s)

    def disable_repl(self):
        uos.dupterm(None, 1)

    def send(self,command, value):
            # empty receive buffer
            if PLATFORM=="EV3":
                if self.uart.waiting()>0:
                    self.uart.read_all()
            else:
                if self.uart.any()!=0:
                    self.uart.read()
            c={'c':command,'v':value}
            cjs=json.dumps(c)
            l=struct.pack('<h',len(cjs))
            self.debug(l+cjs)
            self.uart.write(l+cjs)

    def receive(self):
        if PLATFORM=="EV3":
            while (self.uart.waiting()==0):
                pass
        else:
            while (self.uart.any()==0):
                pass
        ls=self.uart.read(2)
        l=struct.unpack('<h',ls)[0]
        self.debug('rcv %d'%l)
        s=b''
        for i in range(l):
            r=self.uart.read(1)
            if r!=None:
                s+=r
        self.debug(s)
        self.debug('read remaining jnk')
        if PLATFORM=="EV3":
            s=s.decode('utf-8') # EV3 BrickPy json.loads does not accept bytearray
            if self.uart.waiting()>0:
                jnk=self.uart.readall()    
        else:
            if self.uart.any()!=0: # are there any unexpected bytes
                jnk=self.uart.read()
        self.debug('finished reading remaining jnk')
        try:
            ss=json.loads(s)
        except:
            ss={'c':'error','v':'nok'}
        self.debug('return from receive')
        return ss

    def send_receive(self,command,value=None):
        self.send(command,value)
        return self.receive()


    def wait_for_command(self):
        rcv=self.receive()
        command=rcv['c']
        value=rcv['v']
        if command in self.commands:
            if value!=None:
                r=self.commands[command](value)
            else:
                r=self.commands[command]()
            if r!=None:
                self.send(command,rcv)
        else:
            self.send(command,'nok')

    def loop(self):
        while True:
            self.wait_for_command()

