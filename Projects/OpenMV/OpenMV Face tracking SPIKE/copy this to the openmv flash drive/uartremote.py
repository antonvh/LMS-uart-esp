# this library support the following micropython based platforms
# - pybricks on EV3
# - micropython on ESP8266
# - micropython on ESP32
# - micropython on OpenMV H7 plus
# - SPIKE hub
# python3 on any other platform. pyserial is required in that case.

import struct
import sys

EV3=1
ESP32=2
ESP32_S2=3
ESP8266=4
SPIKE=5
H7=7

platforms = {
    'linux':EV3, # EV3. TODO This might not be precise enough for python3 running on Linux laptops
    'esp32':ESP32,
    'Espressif ESP32-S2':ESP32_S2,
    'esp8266':ESP8266,
    'OpenMV4P-H7':H7,
    'LEGO Learning System Hub':SPIKE
}
platform = platforms[sys.platform]


class UartRemoteError(Exception):
    def __init__(self, message="An error occured with remote uart"):
        super().__init__(message)

interrupt_pressed=0

def esp_interrupt(p):
    # called by irq on gpio0
    global interrupt_pressed
    print("Interrupt Pressed")
    dupterm(machine.UART(0, 115200), 1) # repl with 115200baud
    interrupt_pressed=1

if platform==ESP8266:
    from machine import UART
    from machine import Pin
    import machine
    from utime import sleep_ms
    from uos import dupterm
    gpio0=Pin(0,Pin.IN)# define pin0 as input = BOOT button on board
    gpio0.irq(trigger=Pin.IRQ_FALLING, handler=esp_interrupt)
elif platform==ESP32:
    from machine import UART
    from machine import Pin
    import machine
    from utime import sleep_ms
    from uos import dupterm
    #gpio0=Pin(0,Pin.IN)# define pin0 as input = BOOT button on board
    #gpio0.irq(trigger=Pin.IRQ_FALLING, handler=esp_interrupt)
elif platform==ESP32_S2: # circuipython
    from busio import UART
    import board
    from time import sleep
    def sleep_ms(ms):
        sleep(ms/1000)

elif platform==EV3:
    from utime import sleep_ms
    from pybricks.iodevices import UARTDevice
    from pybricks.parameters import Port
elif platform==H7:
    from machine import UART
    from utime import sleep_ms
    from uos import dupterm
elif platform==SPIKE:
    from utime import sleep_ms
    import hub
else:
    from time import sleep
    import serial
    def sleep_ms(ms):
        sleep(ms/1000)

class UartRemote:
    """
    UartRemote
    Use to communicate via REPL or some kind of RPC command loop with other devices.
    """
    commands={}
    command_formats={}

    @staticmethod
    def digitformat(f):
        nn='0'
        i=0
        while f[i]>='0' and f[i]<='9':
                nn+=f[i]
                i+=1
        return (int(nn),f[i:])


    def __init__(self,port=0,baudrate=115200,timeout=1000,debug=False,esp32_rx=0,esp32_tx=26):
        # Baud rates of up to 230400 work. 115200 is the default for REPL.

        self.reads_per_ms = 10
        if platform==EV3:
            if not port: port=Port.S1
            self.uart = UARTDevice(port,baudrate=baudrate,timeout=timeout)
        elif platform==H7:
            self.reads_per_ms = 20
            if not port: port=3
            self.uart = UART(port, baudrate, timeout_char=timeout)
        elif platform==ESP8266:
            self.baudrate=baudrate # store baudrate for repl init
            self.uart = UART(port,baudrate=baudrate,timeout=timeout,timeout_char=timeout,rxbuf=100)
        elif platform==ESP32:
            if not port: port = 1
            self.uart = UART(port,rx=esp32_rx,tx=esp32_tx,baudrate=baudrate,timeout=timeout)
        elif platform==ESP32_S2:
            self.uart = UART(board.TX,board.RX,baudrate=baudrate,timeout=0.5)
        elif platform==SPIKE:
            if type(port) == str:
                self.uart = eval("hub.port."+port)
            else:
                self.uart = port
            self.uart.mode(1)
            sleep_ms(300)# wait for all duplex methods to appear
            self.uart.baud(baudrate) # set baud rate
        else:
            # Try regular python3 pyserial
            self.uart = serial.Serial(port, baudrate, timeout=timeout)
        self.DEBUG=debug
        self.unprocessed_data=b''
        self.baudrate = baudrate
        self.local_repl_enabled = True
        self.add_command(self.enable_repl_locally, name='enable repl')
        self.add_command(self.disable_repl_locally, name='disable repl')
        self.add_command(self.echo, 's', name='echo')
        self.add_command(self.raw_echo, name='raw_echo')


    def echo(self, s):
        if self.DEBUG: print(s)
        return str(s)

    @staticmethod
    def raw_echo(s):
        return s

    def enable_repl_locally(self):
        global interrupt_pressed
        self.local_repl_enabled = True
        interrupt_pressed = 1

    def disable_repl_locally(self):
        self.local_repl_enabled = False

    @property
    def local_repl_enabled(self):
        return self._local_repl_enabled

    @local_repl_enabled.setter
    def local_repl_enabled(self, enabled):
        if enabled:
            if platform==ESP8266:
                dupterm(self.uart, 1)
            elif platform==H7:
                dupterm(self.uart, 2)
        else:
            if platform==ESP8266:
                dupterm(None, 1)
            elif platform==H7:
                dupterm(None, 2)
        self._local_repl_enabled = enabled

    def add_command(self,command_function, format="", name=None):
        if not name:
            name=repr(command_function).split(" ")[1]
        self.commands[name]=command_function
        self.command_formats[name]=format

    def pack(self,*argv):
        try:
            f=argv[0] # formatstring
            i=0
            ff=''
            s=b''
            if f=='raw':
                # No encoding, raw bytes
                # s=struct.pack('B',len(argv[1])) + argv[1]
                s=b'\x03raw'+argv[1]
            else:
                while (len(f)>0):# keep parsing formatstring
                    nf,f=self.digitformat(f) # split preceding digits and format character
                    if nf==0:
                        nf=1
                        fo=f[0]
                        data=argv[1+i]# get data data that needs to be encoded
                        td=type(data) # check type of data
                        if td==list: # for lists, use a special 'a' format character preceding the normal formatcharacter
                            n=len(data)
                            ff+="a%d"%n+fo # 'a' for list
                            for d in data:
                                s+=struct.pack(fo,d) # encode each element in list with format character fo
                        elif td==tuple: # for lists, use a special 'a' format character preceding the normal formatcharacter
                            n=len(data)
                            ff+="t%d"%n+fo # 'a' for list
                            for d in data:
                                s+=struct.pack(fo,d) # encode each element in list with format character fo
                        elif td==str:
                            n=len(data)
                            ff+="%d"%n+fo
                            s+=data.encode('utf-8')
                        elif td==bytes:
                            n=len(data)
                            ff+="%d"%n+fo
                            s+=data
                        else:
                            ff+=fo
                            s+=struct.pack(fo,data)
                    else:
                        fo="%d"%nf+f[0]
                        data=argv[1+i:1+i+nf]
                        ff+=fo
                        s+=struct.pack(fo,*data)
                    i+=nf
                    f=f[1:] # continue parsing with remainder of f
                s=struct.pack('B',len(ff))+ff.encode('utf-8')+s
            return s
        except:
            t=type(argv[0])
            if t==bytes:
                return argv[0]
            elif t==str:
                return bytes(argv[0],"utf-8")
            elif t==int:
                return bytes((argv[0],))
            elif t==list:
                return bytes(argv[0])
            else:
                return b'\x01z'

    def unpack(self,s):
        sizes={'b':1,'B':1,'i':4,'I':4,'f':4,'s':1,'r':1}
        try:
            p=0
            nf=s[p]
            p+=1
            f=s[p:p+nf].decode('utf-8')
            p+=nf
            data=()
            if f=="z":# dummy format 'z' for empty data
                return None
            if f=="raw": # Raw bytes, no decoding needed
                return s[p:]
            while (len(f)>0):
                nf,f=self.digitformat(f)
                fo=f[0]
                if f[0]=='a' or f[0]=='t': # array
                    extra=f[0]
                    f=f[1:]
                    nf,f=self.digitformat(f)
                    fo=f[0]
                    nr_bytes=nf*sizes[fo]
                    if extra=='a':
                        data=data+(list(struct.unpack("%d"%nf+fo,s[p:p+nr_bytes])),) # make list from tuple returnd by unpack
                    else:
                        data=data+(tuple(struct.unpack("%d"%nf+fo,s[p:p+nr_bytes])),) # make list from tuple returnd by unpack
                else:
                    ff=fo if nf==0 else "%d"%nf+fo
                    if nf==0: nf=1
                    nr_bytes=nf*sizes[fo]
                    if ff[-1]=='r': ff=ff[:-1]+'s'
                    decoded=struct.unpack(ff,s[p:p+nr_bytes])
                    if fo=='s':
                        decoded=(decoded[0].decode('utf-8'),) # transform bytes in string
                    data=data+(decoded)
                p+=nr_bytes
                f=f[1:]
            if len(data)==1: # convert from tuple size 1 to single value
                data=data[0]
            return data
        except:
            return s

    def encode(self,cmd,*argv,encoder=-1):
        """ Encodes command with specified encoder """
        if argv:
            if encoder:
                if encoder==-1:
                    encoder=self.pack
                s=encoder(*argv)
            else:
                s=argv[0]
        else: # no formatstring
            s=b'\x01z'# dummy format 'z' for no arguments
        s=struct.pack("B",len(cmd))+cmd.encode('utf-8')+s
        s=struct.pack("B",len(s))+s
        return s

    def decode(self,s,decoder=-1):
        """ Decodes command + encoded bytes with specified decoder"""
        nl=s[0] #number bytes in total length of message
        nc=s[1] #number of bytes in command
        cmd=s[2:2+nc].decode('utf-8')
        data=s[2+nc:]
        if decoder:
            if decoder==-1:
                decoder=self.unpack
            data=decoder(data)
        else:
            if data==b'\x01z': data=None
        return cmd,data


    def available(self):
        """ Platform independent check for available characters in receive queue of UART """
        if platform==SPIKE:
            self.unprocessed_data=self.force_read(1, timeout=1)
            if self.unprocessed_data==None:
                self.unprocessed_data=b''
            return len(self.unprocessed_data)
        if platform==EV3:
            return self.uart.waiting()
        if platform==ESP32 or platform==ESP8266 or platform==H7:
            return self.uart.any()
        if platform==ESP32_S2:
            return self.uart.in_waiting
        else:
            #pyserial
            return self.uart.in_waiting()

    def read_all(self):
        # Read full receive buffer
        available = self.available()
        data = self.unprocessed_data
        if platform == SPIKE:

            self.unprocessed_data = b''
            while True:
                r=self.uart.read(1)
                if r==b'': break
                data += r
        else:
            if available:
                data = self.uart.read(available)

        return data

    def force_read(self, size=1, timeout=50):
        # SPIKE and OpenMV reads too fast and sometimes returns None
        # check: on SPIKE b'' is returned, on OpenMV None
        data = b''
        r=self.uart.read(1)
        for i in range(timeout*self.reads_per_ms):
            if r==None:
                r=b''
            data += r
            if len(data) == size:
                return data
            else:
                r=self.uart.read(1)
            if i > 3 and self.DEBUG:
                print("Waiting for data in force read...")
        return data


    def receive_command(self,timeout=1000,**kwargs):
        global interrupt_pressed

        delim=b''
        if platform==SPIKE:
            if self.unprocessed_data:
                delim = self.unprocessed_data
                self.unprocessed_data=b''

            for i in range(timeout*self.reads_per_ms):
                if delim==b'<':
                    break
                else:
                    delim=self.uart.read(1)

            if delim!=b'<':
                return ("err","< delim not found")

            payload=self.force_read(1)
            l=struct.unpack('B',payload)[0]
            for i in range(l):
                    r = self.force_read(1)
                    payload+=r
            delim=self.uart.read(1)

        else: # other platforms
            for i in range(timeout*self.reads_per_ms):
                data = self.read_all()
                if data: break
            if not data:
                if self.DEBUG: print("No data after timeout")
                return ("err","No data")
            #if self.DEBUG: print("Decoding {}".format(data))
            size = len(data)
            for i in range(size):
                #if self.DEBUG: print(data[i:i+1])
                if data[i:i+1] == b'<':
                    if size >= i+2:
                        l=data[i+1]
                    else:
                        l=self.force_read(1,timeout=10)[0]
                    max_reads = timeout*self.reads_per_ms
                    reads=0
                    while len(data) <= i+l+2: #not enough data, read some more. Maybe it's +2.
                        data += self.read_all()
                        reads+=1
                        if reads > 2 and self.DEBUG:
                            print("Waiting for data in rcv command...")
                        if reads > max_reads:
                            break
                    payload = data[i+1:i+2+l]
                    delim = data[i+2+l:i+3+l]
                    #if self.DEBUG: print("Payload: {}, delim: {}".format(payload,delim))
                    break
        if delim!=b'>':
            return ("err","> delim not found")
        else:
            result = self.decode(payload,**kwargs)
            #if self.DEBUG: print(result)
            return result

    def send_command(self,command,*argv,**kwargs):
        s=self.encode(command,*argv,**kwargs)
        msg=b'<'+s+b'>'
        #if self.DEBUG: print(msg)
        if platform==SPIKE: # on spike send 32-bytes at a time
            window=32
            while len(msg) > window:
                self.uart.write(msg[:window])
                sleep_ms(5)
                msg = msg[window:]
            self.uart.write(msg)
        else:
            self.uart.write(msg)
        self.flush()

    def call(self,command,*args,**kwargs):
        self.send_command(command,*args,**kwargs)
        return self.receive_command(**kwargs)

    def execute_command(self, command, value):
        # name should reflect that it send back respons of exeuted command
        if command in self.commands:
            command_ack=command+"ack"
            try:
                if value!=None:
                    if type(value)==tuple:
                        resp=self.commands[command](*value)
                    else:
                        resp=self.commands[command](value)
                else:
                    resp=self.commands[command]()
            except Exception as e:
                self.send_command('err','s', "Command failed: {}".format(e))
                return
            if resp!=None:
                try:
                    f=self.command_formats[command]
                    if f: # There is a (smart)pack format
                        if type(resp)!=tuple:
                            resp=(resp,) # make a tuple
                        self.send_command(command_ack,f,*resp)
                    else: # user probably wants raw response.
                        self.send_command(command_ack,resp)
                except Exception as e:
                    self.send_command('err','s', "Response packing failed: {}".format(e))
                    return
            else:
                self.send_command(command_ack,'s','ok')
        else:
            #if command[-3:] not in ['ack','err']:# discard any ack from other command
                #self.send_command('err','s','Command not found')
            self.send_command('err','s','Command not found: {}'.format(command))

    def process_uart(self):
        if self.local_repl_enabled:
            self.local_repl_enabled=False
        if self.available():
            self.execute_command(*self.receive_command())
        else:
            if self.DEBUG:
                print("Nothing available. Sleeping 100ms")
                sleep_ms(100)
            else:
                 if platform==H7:
                     sleep_ms(13)
                 else:
                     sleep_ms(1)

    def loop(self):
        global interrupt_pressed
        while True:
            if interrupt_pressed==1:
                interrupt_pressed=0
                break
            self.process_uart()

    def flush(self):
        _ = self.read_all()
        if self.DEBUG: print("Flushed: %r" % _)

    def repl_activate(self):
        self.flush()
        self.send_command('enable repl')
        sleep_ms(300)
        self.uart.write(b"r\x03\x03\x01") # Ctrl-c, Ctrl-c, Ctrl-a
        sleep_ms(300)
        self.flush()
        self.uart.write(b"r\x03\x03\x01") # Ctrl-c, Ctrl-c, Ctrl-a
        sleep_ms(10)
        data = self.read_all()
        if not data[-14:] == b'L-B to exit\r\n>':
            raise UartRemoteError("Raw REPL failed (response: %r)" % data)

    def repl_run(self, command, reply=True, raw_paste=True):
        command_bytes_left = bytes(command, "utf-8")
        window = 128

        if raw_paste:
            self.uart.write(b"\x05A\x01") # Try raw paste
            result = self.force_read(2)
            if self.DEBUG: print(result)
            if result == b'R\x01':
                raw_paste = True
                result = self.uart.read(3) # Should be b'x80\x00\x01' where \x80 is the window size
                window = result[0]
            else:
                raw_paste = False
                self.flush()

        if platform==SPIKE:
            window = 32

        while len(command_bytes_left) > window:
            self.uart.write(command_bytes_left[:window]) # Write our MicroPython command and ctrl-D to execute
            sleep_ms(4)
            result = self.uart.read(1)
            command_bytes_left = command_bytes_left[window:]
        self.uart.write(command_bytes_left+b'\x04')

        if raw_paste:
            data = self.force_read(1)
            if data != b'\x04':
                raise UartRemoteError("could not exec command (response: %r)" % data)
        else:
            sleep_ms(10)
            # check if we could exec command
            data = self.uart.read(2)
            if data != b"OK":
                raise UartRemoteError("could not exec command (response: %r)" % data)

        if reply:
            result = b""
            decoded = []
            while not len(decoded) >= 3: # We need at least 3x'\x04'
                result += self.read_all()
                decoded = result.decode("utf-8").split("\x04")
            try:
                value, error, _ = decoded # The last 5 bytes are b'\r\n\x04\x04>' Between the \x04's there can be an exception.
            except:
                raise UartRemoteError("Unexpected answer from repl: {}".format(result))
            if error:
                if self.DEBUG: print(error)
                return error.strip() # using strip() to remove \r\n at the end.
            elif value:
                return value.strip()
            else:
                return

    def repl_exit(self):
        self.uart.write(b"\x02") # Ctrl-B
