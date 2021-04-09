
from hub import port
from utime import sleep_ms

class WifiBoardError(Exception):
    pass

class WifiBoard():
    def __init__(self, port_string):
        # Initialize serial port. SPIKE And RI hubs only.
        # TODO: make this compatible with EV3/Pybricks
        self.board = eval("port."+port_string)
        self.board.mode(1)
        sleep_ms(60)
        self.board.baud(115200)
        # Flush uart buffer
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
        if not result[-14:] == b'L-B to exit\r\n>': 
            raise WifiBoardError("Raw REPL failed")

    def execute(self, command, debug=True):
        self.board.write(b"\x05A\x01") # Enter raw paste
        sleep_ms(5)
        result = self.board.read(6) # Should be b'R\x01\x80\x00\x01' where \x80 is the window size and the first \x01 says paste mode works
        window = 32 # Although the window is usually advertised as 128 in result[-3], only 32 seems to work on the esp8266
        command_bytes_left = bytes(command,"utf-8")
        while len(command_bytes_left) > window:
            self.board.write(command_bytes_left[:window]) # Write our MicroPython command and ctrl-D to execute
            sleep_ms(4)
            result = self.board.read(1)
            command_bytes_left = command_bytes_left[window:]
        self.board.write(command_bytes_left+b'\x04')
        result = ""
        while not result:
            result = self.read_all()
        try:
            _ , value, error, _ = result.decode("utf-8").split("\x04") # The last 5 bytes are b'\r\n\x04\x04>' Between the \x04's there can be an exception.
        except:
            raise WifiBoardError("Unexpected answer from esp: {}".format(result))
        if error:
            if debug: print(error)
            return error.strip() # using strip() to remove \r\n at the end.
        elif value:
            return value.strip()
        else:
            return