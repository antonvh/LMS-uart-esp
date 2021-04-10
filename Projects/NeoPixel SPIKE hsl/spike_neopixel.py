# Copy this into a SPIKE Prime project
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

    def execute(self, command, wait_ms=0, debug=True):
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
        sleep_ms(wait_ms)
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

# def clamp(value, min_value, max_value):
#     return max(min_value, min(max_value, value))

# def saturate(value):
#     return clamp(value, 0.0, 1.0)

# def hue_to_rgb(h):
#     r = abs(h * 6.0 - 3.0) - 1.0
#     g = 2.0 - abs(h * 6.0 - 2.0)
#     b = 2.0 - abs(h * 6.0 - 4.0)
#     return saturate(r), saturate(g), saturate(b)

# def hsl_to_rgb(h, s, l):
#     r, g, b = hue_to_rgb(h)
#     c = (1.0 - abs(2.0 * l - 1.0)) * s
#     r = (r - 0.5) * c + l
#     g = (g - 0.5) * c + l
#     b = (b - 0.5) * c + l
#     rgb = tuple([int(x*255) for x in (r,g,b)])
#     return rgb

def hsl_to_rgb(h,s,l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2
    r=g=b=int(m*255)
    xx = int((x+m)*255)
    cc = int((c+m)*255)
    if h < 60 or h > 300:
        r=cc
    if 60<=h<120 or 240<=h<300:
        r=xx
    if h<60 or 180<=h<240:
        g=xx
    if 60<=h<180:
        g=cc
    if 120<=h<180 or h>=300:
        b=xx
    if 180<=h<300:
        b=cc
    return (r,g,b)



board = WifiBoard('F')
board.enter_raw_repl()
board.execute('import neopixel')
board.execute('np = neopixel.NeoPixel(machine.Pin(4), 12)')

while True:
    abs_pos = port.E.motor.get()[2]
    hue = port.A.motor.get()[2] % 360
    lightness = port.B.motor.get()[2]%360 / 360
    color = hsl_to_rgb(hue, 1.0, lightness)
    current_led = (abs_pos-90)%360 // 30
    board.execute('np.fill((0,0,0))', wait_ms=10)
    board.execute('np[{}]={}'.format(current_led, color))
    board.execute('np.write()')