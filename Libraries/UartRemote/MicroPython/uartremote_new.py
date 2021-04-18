
# this library support the following micropython based platforms
# - pybricks on EV3
# - micropython on ESP8266
# - micropython on ESP32
# - micropython on OpenMV H7 plus
# - SPIKE hub
# python3 on any other platform. pyserial is required in that case.

"""
@timed_function
def test(n):
    for i in range(n):
        q=u.send_raw("abcde"*4,num_ack=)




"""
import utime

# @timed_function
# Print time taken by a function call

def timed_function(f, *args, **kwargs):
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t) 
        print('Function {} Time = {:6.3f}ms'.format(f.__name__, delta/1000))
        return result
    return new_func

""" example usage

@timed_function
def test():
    utime.sleep_us(10000)
"""

import struct
import sys

EV3='linux' # This might not be precise enough for python3 running on Linux laptops
ESP32='esp32'
ESP8266='esp8266'
H7='OpenMV4P-H7'
SPIKE='LEGO Learning System Hub'

class UartRemoteError(Exception):
    def __init__(self, message="An error occured with remote uart"):
        super().__init__(message)

platform=sys.platform

interrupt_pressed=0

def esp_interrupt(p):
    # called by irq on gpio0
    global interrupt_pressed
    print("Interrupt Pressed")
    uos.dupterm(machine.UART(0, 115200), 1) # repl with 115200baud
    interrupt_pressed=1

if platform==ESP8266 or platform==ESP32:
    from machine import UART
    from machine import Pin
    import machine
    from utime import sleep_ms
    import uos
    #gpio0=Pin(0,Pin.IN)  # define pin0 as input = BOOT button on board
    #gpio0.irq(trigger=Pin.IRQ_FALLING, handler=esp_interrupt)
elif platform==EV3:
    from utime import sleep_ms
    from pybricks.iodevices import UARTDevice
    from pybricks.parameters import Port
elif platform==H7:
    from pyb import UART
    from utime import sleep_ms
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
    
    def __init__(self,port=0,baudrate=115200,timeout=1000,debug=False,esp32_rx=0,esp32_tx=26):
        # Baud rates of up to 230400 work. 115200 is the default for REPL.
        if platform==EV3:
            if not port: port=Port.S1
            self.uart = UARTDevice(port,baudrate=baudrate,timeout=timeout)
        elif platform==H7:
            if not port: port=3
            self.uart = UART(port, baudrate, timeout_char=timeout)
        elif platform==ESP8266:
            self.baudrate=baudrate # store baudrate for repl init
            # uos.dupterm(None, 1) # disable repl
            self.uart = UART(port,baudrate=baudrate,timeout=timeout,timeout_char=timeout,rxbuf=100)
        elif platform==ESP32:
            if not port: port = 1
            self.uart = UART(port,rx=esp32_rx,tx=esp32_tx,baudrate=baudrate,timeout=timeout)
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
        
    
    
    def enable_repl_locally(self):
        if platform in [ESP32, ESP8266]:
            uos.dupterm(self.uart, 1)

    def disable_repl_locally(self):
        if platform in [ESP32, ESP8266]:
            uos.dupterm(None, 1)

    def add_command(self,command,command_function, format=""):
        self.commands[command]=command_function
        self.command_formats[command]=format

    
    def available(self):
        """ Platform independent check for available characters in receive queue of UART """
        if platform==SPIKE:
            self.unprocessed_data=self.uart.read(1)
            return len(self.unprocessed_data)
        if platform==EV3:
            return self.uart.waiting()
        if platform==ESP32 or platform==ESP8266:
            return self.uart.any()
        else:
            #pyserial
            return self.uart.in_waiting()

    def wait_available(self,timeout=1000):
        tstart=utime.ticks_ms()
        while not self.available() and utime.ticks_diff(utime.ticks_ms(),tstart) < timeout:
            pass

    def flush(self):
        # empty receive buffer
        #
        # call naar readall() veroorzaakt timeout op esp van 1s.
        if platform==EV3:
            if self.uart.waiting()>0:
                self.uart.read_all()
        elif platform==SPIKE:
            r=b'1'
            while r:
                r=self.uart.read(1)
        else:
            self.uart.read(self.uart.any())

    def read_all(self):
        if platform==SPIKE:
            result = bytes()
            while True:
                sleep_ms(6)
                data = self.uart.read(1024) # causes timeout on some non-spike platforms
                if not data: break
                result += data
        else:
            result=self.uart.read_all()
        return result

    def receive_raw(self,num_bytes,timeout=1000,num_ack=0):
        """ platform independ receive mathod """
        
        buf=b''
        len_buf=0
        err=None
        tstart=utime.ticks_ms()
        acked=0
        if platform==SPIKE:
            # handle unprocessed data for SPIKE
            if self.unprocessed_data: 
                buf = self.unprocessed_data
                self.unprocessed_data=b''  # in case this function gets called without calling available()
                len_buf=1 # always one bytes read
        
        while len_buf < num_bytes  and  utime.ticks_diff(utime.ticks_ms(),tstart) < timeout:
            c=self.uart.read(1)
            if c:
                buf+=c
                len_buf+=1
                if self.DEBUG: print("buf,len_buf",buf,len_buf)
                if num_ack>0:
                    acked+=1
                    if self.DEBUG: print("acked=",acked)
                    if acked==num_ack:
                        acked=0
                        if self.DEBUG: print("ack send")
                        self.uart.write('a')  # maybe two bytes encoded current received length?
        if self.DEBUG: print("len_buf=",len_buf)
        if len_buf==num_bytes:
            # final ack necessary?
            if num_ack>0 and num_bytes%num_ack!=0:
                if self.DEBUG: print("ack send")
                self.uart.write('a')        
            return buf
        else:
            self.flush()
            return None

    def send_raw(self,buf,num_ack=0):
        acked=num_ack>0
        if num_ack>0: self.flush() # empty receive buffer before start
        if platform==SPIKE: # on spike send 32-bytes at a time
            window=32 if not acked else num_ack
            while len(buf) > window:
                self.uart.write(buf[:window])
                sleep_ms(4)
                buf = buf[window:]
            self.uart.write(buf)
        else:
            if acked:
                while len(buf) > num_ack:
                    self.uart.write(buf[:num_ack])
                    if self.DEBUG: print("wait for ack")
                    self.wait_available() # wait until ack
                    ack=self.receive_raw(1)
                    if self.DEBUG: print("ack received")
                    buf = buf[num_ack:]
                if len(buf)>0:
                    self.uart.write(buf)
                    if self.DEBUG: print("final wait for ack")
                    self.wait_available() # wait until ack
                    ack=self.receive_raw(1)
                    if self.DEBUG: print("final ack received")
            else:
                self.uart.write(buf)
        
        
    def read_all(self):
        if platform==SPIKE:
            result = bytes()
            while True:
                sleep_ms(6)
                data = self.uart.read(1024) # causes timeout on some non-spike platforms
                if not data: break
                result += data
        else:
            result=self.uart.read_all()
        return result

    def enter_raw_repl(self):
        self.flush()
        #self.send_command('enable repl')
        sleep_ms(300)
        self.uart.write(b"r\x03\x03\x01")
        sleep_ms(300)
        self.flush()
        self.uart.write(b"r\x03\x03\x01") # Ctrl-c, Ctrl-c, Ctrl-a
        result = self.read_all()
        if self.DEBUG: print("readall=",result)
        if not result[-14:] == b'L-B to exit\r\n>':
            raise UartRemoteError("Raw REPL failed")

    def execute_repl(self, command, reply=True):
        self.uart.write(b"\x05A\x01") # Enter raw paste
        sleep_ms(5)
        result = self.uart.read(6) # Should be b'R\x01\x80\x00\x01' where \x80 is the window size and the first \x01 says paste mode works
        if platform==SPIKE:
            window = 32 # Although the window is usually advertised as 128 in result[-3], only 32 seems to work on the esp8266
        else:
            window = struct.unpack("B", result[-3])[0]
        command_bytes_left = bytes(command, "utf-8")
        while len(command_bytes_left) > window:
            self.uart.write(command_bytes_left[:window]) # Write our MicroPython command and ctrl-D to execute
            sleep_ms(4)
            result = self.uart.read(1)
            command_bytes_left = command_bytes_left[window:]
        self.uart.write(command_bytes_left+b'\x04')
        if reply:
            result = ""
            while not len(result) >= 3: # We need at least 3x'\x04'
                result = self.read_all()
            try:
                _ , value, error, _ = result.decode("utf-8").split("\x04") # The last 5 bytes are b'\r\n\x04\x04>' Between the \x04's there can be an exception.
            except:
                raise UartRemoteError("Unexpected answer from repl: {}".format(result))
            if error:
                if self.DEBUG: print(error)
                return error.strip() # using strip() to remove \r\n at the end.
            elif value:
                return value.strip()
            else:
                return   

    