"""
from uartcmds import *
u=UartComm(0)
u.addcmd('grid',grideye)
u.addcmd('led',led)

"""

# check platform

PLATFORM="EV3"
try:
    from pybricks.iodevices import UARTDevice
except:
    PLATFORM="ESP8266"

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



class UartComm:
    cmds={}

    def __init__(self,port,baud=115200,timeout=1000,debug=False):
        if PLATFORM=="EV3":
            self.uart = UARTDevice(port,baudrate=baud,timeout=timeout)
        else:
            self.uart = UART(port,baudrate=baud,timeout=timeout,rxbuf=100)
        self.DEBUG=debug

    def addcmd(self,cmd,cmd_func):
        self.cmds[cmd]=cmd_func

    def debug(self,s):
        if self.DEBUG:
            print(s)

    def disablerepl(self):
        uos.dupterm(None, 1)

    def snd(self,cmd, value):
            # empty receive buffer
            if PLATFORM=="EV3":
                if self.uart.waiting()>0:
                    self.uart.read_all()
            else:
                if self.uart.any()!=0:
                    self.uart.read()
            
            c={'c':cmd,'v':value}
            cjs=json.dumps(c)
            l=struct.pack('<h',len(cjs))
            self.debug(l+cjs)
            self.uart.write(l+cjs)

    def rcv(self):
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
        self.debug('return from rcv')
        return ss

    def sndrcv(self,cmd,value=None):
        self.snd(cmd,value)
        return self.rcv()


    def waitcmd(self):
        a=self.rcv()
        cmd=a['c']
        val=a['v']
        if cmd in self.cmds:
            if val!=None:
                r=self.cmds[cmd](val)
            else:
                r=self.cmds[cmd]()
            if r!=None:
                self.snd(cmd,r)
        else:
            self.snd(cmd,'nok')

    def loop(self):
        while True:
            self.waitcmd()

def led(v):
    print('led')
    for i in v:
        print(i)
    return 'ok'

def imu():
    return([12.3,11.1,180.0])

def grideye(addr):
    a=[20,21,22,23,24,25,26,27,28]
    return a[addr%9]


def mag():
    x, y, z = mag_sensor.read()                                                                 
    return [x,y,z]   

 

# init devices
mag_sensor = HMC5883L(scl=5,sda=4) 

# set rxbuf to 100 bytes
uart = UART(0, baudrate=115200,rxbuf=100)
# disable repl on uart
uos.dupterm(None, 1)


com = UartCom(0)
