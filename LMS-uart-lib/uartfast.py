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

    def encode(self,cmd,*argv):
        f=argv[0]
        if len(argv)==2:
            data=argv[1]
            td=type(data).__name__
            nf=struct.pack('B',len(f))
            if td=='list': 
                n=len(data)
                ff="a%d"%n+f
                s=struct.pack('B',len(ff))+ff.encode('utf-8')
                for d in data:
                    s+=struct.pack(f,d)
            elif td=='str':
                n=len(data)
                ff="%d"%n+f
                s=struct.pack('B',len(ff))+ff.encode('utf-8')
                s+=data.encode('utf-8')
        else:
            s=struct.pack("B",len(f))+f.encode('utf-8')
            s+=struct.pack(f,*argv[1:])
        s=struct.pack("B",len(cmd))+cmd.encode('utf-8')+s
        s=struct.pack("B",len(s))+s 
        return s 

    def decode(self,s):
        p=1
        nc=struct.unpack('B',s[p:p+1])[0]
        p+=1
        cmd=s[p:p+nc].decode('utf-8')
        p+=nc
        nf=struct.unpack('B',s[p:p+1])[0]
        p+=1
        f=s[p:p+nf].decode('utf-8')
        p+=nf
        if f[0]=='a':
            data=list(struct.unpack(f[1:],s[p:]))
        else:
            data=struct.unpack(f,s[p:])
            if len(data)==1:
                data=data[0]
        return cmd,data

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
        for i in range(l):
            r=self.uart.read(1)
            if r!=None:
                s+=r
        result=self.decode(s)
        #except:
        #    result=("err",[])
        return result


    def send(self,command,*argv):
        s=self.encode(command,*argv)
        self.uart.write(s)


    def send_receive(self,command,*args):
        self.flush()
        self.send(command,*args)
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
                    self.send(command_ack,t,data)
                else:
                    self.send(command_ack,'s','ok')
            else:
                self.send('error','s','nok')

    def loop(self):
        while True:
            self.wait_for_command()

