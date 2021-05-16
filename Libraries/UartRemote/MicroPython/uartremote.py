# Symmetrical communication library for Micropython devices
# (c) 2021 Ste7an, Anton Vanhoucke

import struct
import sys

EV3=1
ESP32=2
ESP32_S2=3
ESP8266=4
SPIKE=5
H7=7
MAC=6

platforms = {
    'linux':EV3, # EV3. TODO This might not be precise enough for python3 running on Linux laptops
    'esp32':ESP32,
    'Espressif ESP32-S2':ESP32_S2,
    'esp8266':ESP8266,
    'OpenMV4P-H7':H7,
    'LEGO Learning System Hub':SPIKE,
    'darwin':MAC
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
    dupterm(UART(0, 115200), 1) # repl with 115200baud
    interrupt_pressed=1

if platform==ESP8266:
    from machine import UART
    from machine import Pin
    from utime import sleep_ms
    from uos import dupterm
    gpio0=Pin(0,Pin.IN)# define pin0 as input = BOOT button on board
    gpio0.irq(trigger=Pin.IRQ_FALLING, handler=esp_interrupt)
elif platform==ESP32:
    from machine import UART
    from machine import Pin
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
    version="May 13, 2021, 00:45"

    def __init__(self,port=0,baudrate=115200,timeout=1500,debug=False,esp32_rx=0,esp32_tx=26):
        # Baud rates of up to 230400 work. 115200 is the default for REPL.
        # Timeout is the time the lib waits in a receive_comand() after placing a call().
        self.local_repl_enabled = False
        self.reads_per_ms = 1
        if platform==EV3:
            if not port: port=Port.S1
            self.uart = UARTDevice(port,baudrate=baudrate,timeout=1)
        elif platform==H7:
            self.reads_per_ms = 20
            self.enable_repl_locally()
            if not port: port=3
            # self.uart = UART(port, baudrate, timeout_char=timeout)
        elif platform==ESP8266:
            self.enable_repl_locally()            
            # self.uart = UART(port,baudrate=baudrate,timeout=timeout,timeout_char=timeout,rxbuf=100)
        elif platform==ESP32:
            if not port: port = 1
            self.uart = UART(port,rx=esp32_rx,tx=esp32_tx,baudrate=baudrate,timeout=1)
        elif platform==ESP32_S2:
            self.uart = UART(board.TX,board.RX,baudrate=baudrate,timeout=0.5)
        elif platform==SPIKE:
            self.reads_per_ms = 10
            if type(port) == str:
                self.uart = eval("hub.port."+port)
            else:
                self.uart = port
            self.uart.mode(1)
            sleep_ms(300)# wait for all duplex methods to appear
            self.uart.baud(baudrate) # set baud rate
        else:
            # Try regular python3 pyserial
            self.uart = serial.Serial(port, baudrate, timeout=1)
        self.DEBUG=debug
        self.unprocessed_data=b''
        self.port = port
        self.timeout=timeout
        self.baudrate=baudrate # store baudrate for repl init
        self.add_command(self.enable_repl_locally, name='enable repl')
        self.add_command(self.disable_repl_locally, name='disable repl')
        self.add_command(self.echo, 'repr', name='echo')
        self.add_command(self.raw_echo, name='raw echo')

    def echo(self, *s):
        if self.DEBUG: print(s)
        return s

    @staticmethod
    def raw_echo(s):
        return s

    def enable_repl_locally(self):
        global interrupt_pressed
        interrupt_pressed = 1 # Break any running ur.loop() before turning REPL on
        if platform==ESP8266:
            # Hard coded default ESP8266 values:
            dupterm(UART(0, 115200), 1)
            self.local_repl_enabled = True
        elif platform==H7:
            # Hard coded default H7 values:
            dupterm(UART(3, 115200), 2)
            self.local_repl_enabled = True
        else:
            self.local_repl_enabled = False

    def disable_repl_locally(self):
        self.local_repl_enabled = False
        if platform==ESP8266:
            dupterm(None, 1)
            self.uart = UART(self.port,baudrate=self.baudrate,timeout=1,timeout_char=1,rxbuf=100)
        elif platform==H7:
            dupterm(None, 2)
            self.uart = UART(self.port,baudrate=self.baudrate,timeout_char=1)

    def add_command(self,command_function, format="", name=None):
        if not name:
            name=repr(command_function).split(" ")[1]
        self.commands[name]=command_function
        self.command_formats[name]=format

    @staticmethod
    def encode(cmd,*argv):
        if argv:
            try:
                f=argv[0]
                if f=='raw':
                    # No encoding, raw bytes
                    s=b'\x03raw'+argv[1]
                elif f=='repr':
                    # use a pickle-like encoding to send any Python object.
                    s=b'\x04repr'+repr(argv[1:]).encode()
                else:
                    # struct pack
                    s = bytes((len(f),)) + f.encode() + struct.pack(f, *argv[1:])
            except:
                # raise
                t=type(argv[0])
                if t==bytes:
                    s = argv[0]
                elif t==str:
                    s = bytes(argv[0],"utf-8")
                elif t==int:
                    s = bytes((argv[0],))
                elif t==list:
                    s = bytes(argv[0])
                else:
                    s = b'\x01z'
        else: # no formatstring
            s=b'\x01z'# dummy format 'z' for no arguments
        s=bytes((len(cmd),))+cmd.encode('utf-8')+s
        s=bytes((len(s),))+s
        return s

    @staticmethod
    def decode(s):
        nc=s[1] #number of bytes in command
        cmd=s[2:2+nc].decode('utf-8')
        data=s[2+nc:]
        if data==b'\x01z': 
            data=None
        else:
            try:
                p=data[0]+1
                f=data[1:p]
                if f==b"raw": # Raw bytes, no decoding needed
                    data = data[p:]
                elif f==b"repr":
                    d={}
                    text = data[p:].decode('utf-8')
                    if "(" in text:
                        qualname = text.split("(", 1)[0]
                        if "." in qualname:
                            pkg = qualname.rsplit(".", 1)[0]
                            mod = __import__(pkg)
                            d[pkg] = mod
                    data = eval(text, d)
                else:
                    data=struct.unpack(f,data[p:])
                if len(data)==1:
                    # convert from tuple size 1 to single value
                    data=data[0]
            except:
                # Pass data as raw bytes
                pass
        return cmd,data

    def available(self):
        # Platform independent check for available characters in receive queue of UART
        if platform==SPIKE:
            self.unprocessed_data=self.uart.read(1)
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

    def flush(self):
        _ = self.read_all()
        if self.DEBUG: print("Flushed: %r" % _)
        
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

    def receive_command(self,timeout=-2):
        # Set timeout to -1 to wait forever.
        if timeout == -2: timeout = self.timeout
        if self.local_repl_enabled: self.disable_repl_locally()
        delim=b''
        if platform==SPIKE or platform==ESP8266:
            if self.unprocessed_data:
                delim = self.unprocessed_data
                self.unprocessed_data=b''
            i=0
            while True:
                if delim==b'<': break
                elif i >= timeout*self.reads_per_ms and timeout != -1: break
                else: 
                    delim=self.uart.read(1)
                    i+=1

            if delim!=b'<':
                err = "< delim not found after timeout of {}".format(timeout)
                if self.DEBUG: print(err)
                return ("err",err)

            payload=self.force_read(1)
            l=struct.unpack('B',payload)[0]
            for i in range(l):
                    r = self.force_read(1)
                    payload+=r
            delim=self.uart.read(1)

        else: # other platforms like H7
            i=0
            while True:
                data = self.read_all()
                i+=1
                if data: break
                if i > timeout*self.reads_per_ms and timeout > 0: break
            if not data:
                err="No data after timeout of {}".format(timeout)
                if self.DEBUG: print(err)
                return ("err",err)
            
            size = len(data)
            for i in range(size):
                if data[i:i+1] == b'<':
                    if size >= i+2:
                        l=data[i+1]
                    else:
                        l=self.force_read(1,timeout=10)[0]
                    max_reads = timeout*self.reads_per_ms
                    reads=0
                    while len(data) <= i+l+2: #not enough data, read some more.
                        data += self.read_all()
                        reads+=1
                        if reads > 2 and self.DEBUG:
                            print("Waiting for data in rcv command...")
                        if reads > max_reads:
                            break
                    payload = data[i+1:i+2+l]
                    delim = data[i+2+l:i+3+l]
                    break
        if delim!=b'>':
            if self.DEBUG: print("Delim {}".format(delim))
            return ("err","> delim not found")
        else:
            result = self.decode(payload)
            return result

    def send_command(self,command,*argv):
        if self.local_repl_enabled: self.disable_repl_locally()
        s=self.encode(command,*argv)
        msg=b'<'+s+b'>'
        if platform==SPIKE: # On spike send 32-bytes at a time
            window=32
            while len(msg) > window:
                self.uart.write(msg[:window])
                sleep_ms(5)
                msg = msg[window:]
            self.uart.write(msg)
        else:
            self.uart.write(msg)

    def call(self,command,*args,**kwargs):
        # Send a command to a remote host that is waiting for a call. 
        # wait until an answer comes.
        # Timeout for the answer is self.timout, or passable as timeout=...
        self.send_command(command,*args)
        self.flush() # Clear the uart buffer so it's ready to pick up an answer
        return self.receive_command(**kwargs)

    def reply_command(self, command, value):
        # Process command(value) and send_command() with the result and an ack.
        if command in self.commands:
            try:  # executing command
                if value!=None:
                    if type(value)==tuple:
                        resp=self.commands[command](*value)
                    else:
                        resp=self.commands[command](value)
                else:
                    resp=self.commands[command]()
            except Exception as e:
                self.ack_err(command=command, value="Command failed: {}".format(e))
                return

            try: # packing and sensing the result
                self.ack_ok(command, self.command_formats[command], resp)
            except Exception as e:
                self.ack_err(command=command, msg="Response packing failed: {}".format(e))
                return
        else:
            self.ack_err(command=command, msg='Command not found: {}'.format(command))

    def ack_ok(self, command="",fmt="2s", resp="ok"):
        command_ack=command+"ack"
        if type(resp) == tuple:
            # Command has returned multiple values in a tuple. Unpack the tuple
            args=(fmt, *resp) 
        else:
            args=(fmt,resp)
        self.send_command(command_ack,*args)

    def ack_err(self, command="",fmt="repr", msg="not ok"):
        command_err=command+"err"
        if self.DEBUG: print(msg)
        self.send_command(command_err,fmt,msg)

    def process_uart(self, sleep=-2):
        # Answer a call if there is one:
        # Receive an incoming command
        # Process the results with any commands from commands[].
        # Reply with the answer.
        # Sleep for sleep ms after every listen.
        if sleep == -2:
            if platform == H7: 
                sleep=13
            else:
                sleep=1
        if self.local_repl_enabled: self.disable_repl_locally()
        if self.available():
            self.reply_command(*self.receive_command())
        else:
            if self.DEBUG:
                print("Nothing available. Sleeping 1000ms")
                sleep_ms(1000)
            else:
                sleep_ms(sleep)

    def loop(self):
        # Loop forever and check for incoming calls
        # You can create a similar loop yourself and your own control code to it.
        global interrupt_pressed
        interrupt_pressed=0
        while True:
            if interrupt_pressed==1:
                interrupt_pressed=0
                break
            self.process_uart()
        self.enable_repl_locally()

    def repl_activate(self):
        # Cajole the other side into a raw REPL with a lot of ctrl-c and ctrl-a.
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
        # Execute MicroPython remotely via raw repl.
        # RAW repl must be activated first!
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
                raise UartRemoteError("Could not send command (response: %r)" % data)
        else:
            sleep_ms(10)
            # Check if we could send command
            data = self.uart.read(2)
            if data != b"OK":
                raise UartRemoteError("Could not send command (response: %r)" % data)

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

