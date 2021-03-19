from hub import port
from utime import sleep_ms

# Connect the breakout board with wifi to port C
# Connect a motor to port B and turn it to control the relais

class WifiBoard():
    def __init__(self, port_string):
        # Initialize serial port
        self.board = eval("port."+port_string)
        self.board.mode(1)
        sleep_ms(50)
        self.board.baud(115200)
        # Flush
        data = "yes"
        while data:
            data = self.board.read(1024)

    def read_all(self):
        result = bytes()
        while True:
            sleep_ms(6)
            data = self.board.read(1024)
            if not data: break
            result += data
        return result

    def enter_raw_repl(self):
        self.board.write(b"r\x03\x03\x01") # Ctrl-c, Ctrl-c, Ctrl-a
        result = self.read_all()
        if not result[-14:] == b'L-B to exit\r\n>': return "Raw repl failed"

    def execute(self, command, result_pause=10):
        self.board.write(b"\x05A\x01") # Enter raw paste
        sleep_ms(5)
        result = self.board.read(6) # Should be b'R\x01\x80\x00\x01' where \x80\x00 is the window size and the first \x01 says paste mode works
        self.board.write(bytes(command,"utf-8")+b"\x04") # Write our MicroPython command and ctrl-D to execute
        result = self.read_all()
        _ , value, error, _ = result.decode("utf-8").split("\x04") # The last 5 bytes are b'\r\n\x04\x04>' Between the \x04's there can be an exception.
        if error:
            return error.strip() # using strip() to remove \r\n at the end.
        else:
            return value.strip()



wifi = WifiBoard('C')
mb = port.B.motor

wifi.enter_raw_repl()
wifi.execute("from machine import Pin")
wifi.execute("p4 = Pin(4, Pin.OUT)")
while True:
    absolute_pos = mb.get()[2]
    if absolute_pos > 0:
        wifi.execute("p4.value(1)")
    else:
        wifi.execute("p4.value(0)")