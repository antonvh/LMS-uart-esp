
# this library support the following micropython based platforms
# - pybricks on EV3
# - micropython on ESP8266
# - micropython on ESP32
# - micropython on OpenMV H7 plus
# - SPIKE hub

platforms={'linux':'EV3','esp32':'ESP32','esp8266':'ESP8266',\
            'OpenMV4P-H7':'H7','LEGO Learning System Hub':'SPIKE'
            }

import sys
platform='unknown'
try:
    platform=sys.platform
    PLATFORM=platforms[platform]
except:
    print("Platform {} unknown.".format(platform))
    exit()

import struct
import time
import sys

interrupt_pressed=0

def esp_interrupt(p):
    global interrupt_pressed
    print("Interrupt Pressed")
    interrupt_pressed=1

if PLATFORM=="ESP8266" or PLATFORM=="ESP32":
    from machine import UART
    from machine import Pin,I2C
    gpio0=Pin(0,Pin.IN)  # define pin0 as input = BOOT button on board
    gpio0.irq(trigger=Pin.IRQ_FALLING, handler=esp_interrupt)
    #from compas import *
    import uos
elif PLATFORM=="EV3":
    from pybricks.iodevices import UARTDevice
    from pybricks.parameters import Port
elif PLATFORM=="H7":
    from pyb import UART
elif PLATFORM=="SPIKE":
    from hub import port
    from utime import sleep_ms

class UartRemote:
    """UartRemote class"""
    commands={}
    command_formats={}
    
    def digitformat(self,f):
        nn='0'
        i=0
        while f[i]>='0' and f[i]<='9':
                nn+=f[i]
                i+=1
        return (int(nn),f[i:])


    def __init__(self,*port_lego,baudrate=230400,timeout=1000,debug=False):
        if PLATFORM=="EV3":
            port=port_lego[0]
            self.uart = UARTDevice(port,baudrate=baudrate,timeout=timeout)
        elif PLATFORM=="H7":
            self.uart = UART(3, baudrate, timeout_char=timeout)
        elif PLATFORM=="ESP8266":
            self.uart = UART(0,baudrate=baudrate,timeout=timeout,timeout_char=timeout,rxbuf=100)
        elif PLATFORM=="ESP32":
            self.uart = UART(1,rx=18,tx=19,baudrate=baudrate,timeout=timeout)
        elif PLATFORM=="SPIKE":
            port=port_lego[0]
            self.uart = port
            self.uart.mode(1)
            sleep_ms(1000)# wait for all duplex methods to appear
            self.uart.baud(baudrate) # set baud rate
            self.last_char=b''
        else:
            raise RuntimeError('MicroPython Platform not defined')
        self.DEBUG=debug

    def add_command(self,command,*argv):
        if len(argv)==1: # no formatstring
            self.command_formats[command]=""
        else: 
            self.command_formats[command]=argv[1]
        self.commands[command]=argv[0]

    def encode(self,cmd,*argv):
        if len(argv)>0:
            f=argv[0]
            i=0
            ff=''
            s=b''
            f=argv[0]
            while (len(f)>0):
                nf,f=self.digitformat(f)
                if nf==0:
                    nf=1
                    fo=f[0]
                    data=argv[1+i]
                    td=type(data)
                    if td==list:
                        n=len(data)
                        ff+="a%d"%n+fo
                        for d in data:
                            s+=struct.pack(fo,d)
                    elif td==str:
                        n=len(data)
                        ff+="%d"%n+fo
                        s+=data.encode('utf-8')
                    else:
                        ff+=fo
                        s+=struct.pack(fo,data)

                else:
                    fo="%d"%nf+f[0]
                    data=argv[1+i:1+i+nf]
                    ff+=fo
                    s+=struct.pack(fo,*data)
                i+=nf
                f=f[1:]
            s=struct.pack('B',len(ff))+ff.encode('utf-8')+s
        else:
            s=b'\x01z'# dummy format 'z' for no arguments
        s=struct.pack("B",len(cmd))+cmd.encode('utf-8')+s
        s=struct.pack("B",len(s))+s
        return s

    def decode(self,s):
        sizes={'b':1,'B':1,'i':4,'I':4,'f':4,'s':1}
        nl=struct.unpack('B',s[:1])[0]
        p=1
        nc=struct.unpack('B',s[p:p+1])[0]
        p+=1
        cmd=s[p:p+nc].decode('utf-8')
        p+=nc
        nf=struct.unpack('B',s[p:p+1])[0]
        p+=1
        f=s[p:p+nf].decode('utf-8')
        p+=nf
        data=()
        if f=="z":# dummy format 'z' for empty data
            return cmd,None
        while (len(f)>0):
            nf,f=self.digitformat(f)
            fo=f[0]
            if f[0]=='a': # array
                f=f[1:]
                nf,f=self.digitformat(f)
                fo=f[0]
                nr_bytes=nf*sizes[fo]
                data=data+(list(struct.unpack("%d"%nf+fo,s[p:p+nr_bytes])),)
            else:
                ff=fo if nf==0 else "%d"%nf+fo
                if nf==0: nf=1
                nr_bytes=nf*sizes[fo]
                data=data+(struct.unpack(ff,s[p:p+nr_bytes]))
            p+=nr_bytes
            f=f[1:]
        if len(data)==1: # convert from tuple size 1 to single value
            data=data[0]
        if nl!=p-1:
            return "error","len"
        else:
            return cmd,data
    def available(self):
        if PLATFORM=="SPIKE":
            self.last_char=self.uart.read(1)
            if self.last_char==b'':
                return 0
            else:
                return 1
        if PLATFORM=="EV3":
            return self.uart.waiting()
        else:
            return self.uart.any()

    def flush(self):
        # empty receive buffer
        if PLATFORM=="EV3":
            if self.uart.waiting()>0:
                self.uart.read_all()
        elif PLATFORM=="SPIKE":
            r=b'1'
            while r!=b'':
                r=self.uart.read(1)
        else:
            if self.uart.any()!=0:
                self.uart.read()

    def receive(self):
        global interrupt_pressed 
        delim=b""
        if PLATFORM=="EV3":
            while (self.uart.waiting()==0):
                pass
        elif PLATFORM=="SPIKE":
            if self.last_char==b'':
                c=b''
                while c==b'':
                    c=self.uart.read(1)
                delim=c
            else:
                delim=self.last_char # in self.available() the first non zero character is stored in self.last_char
                self.last_char=b''
        elif PLATFORM=="ESP8266":
            while (self.uart.any()==0):
                if interrupt_pressed==1:
                    interrupt_pressed=0
                    break
                else:
                    pass
        elif PLATFORM=="H7":
            while (self.uart.any()==0):
                time.sleep(0.01)
                pass
        else:
            while (self.uart.any()==0):
                pass
        try:
            if delim==b'':
                delim=self.uart.read(1)
            if delim!=b'<':
                self.flush()
                return ("err","nok")
            ls=self.uart.read(1)
            l=struct.unpack('B',ls)[0]
            s=ls
            for i in range(l):
                # OpenMV reads too fast and sometimes returns None
                r=None
                while r==None:
                    r=self.uart.read(1)
                s+=r
            delim=self.uart.read(1)
            if delim!=b'>':
                self.flush()
                return ("err","nok")
            else:
                result=self.decode(s)

        except:
            self.flush()
            result=("err","nok")
        return result


    def send(self,command,*argv):
        try:
            s=self.encode(command,*argv)
            msg=b'<'+s+b'>'
            if PLATFORM=="SPIKE": # on spike send 32-bytes at a time
                window=32
                while len(msg) > window:
                    self.uart.write(msg[:window])
                    sleep_ms(4)
                    msg = msg[window:]
                self.uart.write(msg)
            else:
                self.uart.write(msg)
                return 1
        except:
            self.flush()
            return 0


    def send_receive(self,command,*args):
        self.flush()
        try:
            self.send(command,*args)
            return self.receive()
        except:
            self.flush()
            return ("err","nok")


    def wait_for_command(self):
        command,value=self.receive()
        if command[-3:]!='ack':# discard any ack from other command
            if command in self.commands:
                command_ack=command+"ack"
                if value!=None:
                    if type(value)==tuple:
                        resp=self.commands[command](*value)
                    else:
                        resp=self.commands[command](value)
                else:
                    resp=self.commands[command]()
                if resp!=None:
                    f=self.command_formats[command]
                    if type(resp)!=tuple:
                        resp=(resp,) # make a tuple
                    self.send(command_ack,f,*resp)
                else:
                    self.send(command_ack,'s','ok')
            else:
                self.send('err','s','nok')

    def loop(self):
        global interrupt_pressed
        while True:
            if interrupt_pressed==1:
                interrupt_pressed=0
                break
            try:
                self.wait_for_command()
            except:
                self.flush()


