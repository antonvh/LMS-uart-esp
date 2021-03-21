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

import struct

if PLATFORM=="ESP8266":
    from machine import UART
    from machine import Pin,I2C
    #from compas import *
    import uos
elif PLATFORM=="EV3":
    from pybricks.iodevices import UARTDevice
    from pybricks.parameters import Port
elif PLATFORM=="H7":
    from pyb import UART


"""

<l><lc><cmd><n><t><data>

<l> = total length of packet
<lc> = length command string
<cmd> = command (3 characters)
<n> = number of data elements
<t> = type of data , struct 'b'=byte, etc
"""



class UartRemote:
    commands={}  
 
    def __init__(self,port,baudrate=230400,timeout=1000,debug=False):
        if PLATFORM=="EV3":
            self.uart = UARTDevice(port,baudrate=baudrate,timeout=timeout)
        elif PLATFORM=="H7":
            self.uart = UART(3, baudrate, timeout_char=timeout)                         # P4,P5 default self.uart
        elif PLATFORM=="ESP8266":    
            self.uart = UART(port,baudrate=baudrate,timeout=timeout,rxbuf=100)
        else:
            raise RuntimeError('MicroPython Platform not defined')
        self.DEBUG=debug

    def add_command(self,command,command_function):
        self.commands[command]=command_function

    def encode(self,command,t,data):
        lc=len(command)
        n=len(data)
        s=struct.pack("B",lc)
        s+=command.encode('utf-8')
        s+=struct.pack("B",n)
        s+=t.encode('utf-8')
        for i in data:
            s+=struct.pack(t,i)
        l=len(s)+1
        s=struct.pack("B",l)+s
        return s

    def decode(self,s):
        l,lc=struct.unpack("BB",s[:2])
        cmd=s[2:2+lc]
        n=struct.unpack("B",s[2+lc:3+lc])[0]
        t=s[3+lc:4+lc].decode('utf-8')
        tt=t*n
        ss=list(struct.unpack(tt,s[4+lc:]))
        command=cmd.decode('utf-8')
        return command,ss

    def available(self):
        if PLATFORM=="EV3":
            return self.uart.waiting()
        else:
            return self.uart.any()

    def flush(self):
        # empty receive buffer
        if PLATFORM=="EV3":
            if self.uart.waiting()>0:
                self.uart.read_all()
        else:
            if self.uart.any()!=0:
                self.uart.read()
        
    def receive(self):
        if PLATFORM=="EV3":
            while (self.uart.waiting()==0):
                pass
        else:
            while (self.uart.any()==0):
                pass
        #try:
        ls=self.uart.read(1)
        l=struct.unpack('B',ls)[0]
        #print(l+1)
        s=ls
        for i in range(l-1):
            r=self.uart.read(1)
            if r!=None:
                s+=r
        result=self.decode(s)
        #except:
        #    result=("err",[])
        return result


    def send(self,command,t,data):
        s=self.encode(command,t,data)
        self.uart.write(s)


    def send_receive(self,command,*args):
        self.flush()
        if len(args)==0:
            t='B'
            data=[]
        else:
            t=args[0]
            data=args[1]
        typename=type(data).__name__
        if typename!='list' and typename!='str':
            data=[args[1]] # make an array
        self.send(command,t,data)
        return self.receive()


    def wait_for_command(self):
        command,value=self.receive()
        if command[-3:]!='ack':   # discard any ack from other command
            if command in self.commands:
                command_ack=command+"ack"
                if value!=[]:
                    resp=self.commands[command](value)
                else:
                    resp=self.commands[command]()
                if resp!=None:
                    t=resp[0]
                    data=resp[1]
                    if type(data).__name__!='list':
                        data=[data]
                    self.send(command_ack,t,data)
                else:
                    self.send(command_ack,'s','')
            else:
                self.send('error','s','nok')

    def loop(self):
        while True:
            self.wait_for_command()

