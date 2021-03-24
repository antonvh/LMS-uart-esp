from hub import port
from utime import sleep_ms

# Control the position of a neopixel led on the wifi board using motor B
# Connect the wifi breakout board with wifi to port C on robot inventor
# Connect a motor to port B and turn it to control the led position

class WifiBoardError(Exception):
    pass

class WifiBoard():
    def __init__(self, port_string):
        # Initialize serial port
        self.board = eval("port."+port_string)
        self.board.mode(1)
        sleep_ms(60)
        self.board.baud(115200)
        # Flush uart buffer
        _ = self.read_all()

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
        window = 32 # Although the window size is usually advertised as 128 in result[-3], only 32 seems to work on the esp8266
        command_bytes_left = bytes(command,"utf-8")
        while len(command_bytes_left) > window:
            self.board.write(command_bytes_left[:window]) # Write our MicroPython command up to the window size
            sleep_ms(4) # Wait for the esp to process the buffer
            result = self.board.read(1) # Check for errors, should be empty.
            command_bytes_left = command_bytes_left[window:] # Delete the bytes that have already been sent.
        self.board.write(command_bytes_left+b'\x04') # and ctrl-D to execute
        result = ""
        while not result: # Keep reading until the wifiboard to responds.
            result = self.read_all()
        try:
            _ , value, error, _ = result.decode("utf-8").split("\x04") 
            # The last 5 bytes are b'\r\n\x04\x04>' Between the \x04's there can be an exception.
        except:
            raise WifiBoardError("Unexpected answer from esp: {}".format(result))
        if error:
            if debug: print(error)
            return error.strip() # using strip() to remove \r\n at the end.
        elif value:
            return value.strip()
        else:
            return

wifi = WifiBoard('C')
mb = port.B.motor

wifi.enter_raw_repl()
wifi.execute("import neopixel, machine")
wifi.execute("p4 = machine.Pin(4)")
wifi.execute("np = neopixel.NeoPixel(p4,12)")

## Run some tests
# print(wifi.execute("print(123)"))
# wifi.execute("np[1] = (255,0,0)")
# wifi.execute("np.write()")

N_LEDS = 12

# These functions are for converting hsl to rgb
# With hsl it is easier to shift hues and lightnesses

def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def saturate(value):
    return clamp(value, 0.0, 1.0)

def hue_to_rgb(h):
    r = abs(h * 6.0 - 3.0) - 1.0
    g = 2.0 - abs(h * 6.0 - 2.0)
    b = 2.0 - abs(h * 6.0 - 4.0)
    return saturate(r), saturate(g), saturate(b)

def hsl_to_rgb(h, s, l):
    r, g, b = hue_to_rgb(h)
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    r = (r - 0.5) * c + l
    g = (g - 0.5) * c + l
    b = (b - 0.5) * c + l
    rgb = tuple([int(x*255) for x in (r,g,b)])
    return rgb

def gauss1(x):
    # If x is in range (0, 100) return a number between 0 and 0.5
    # According to a guassian distribution
    # This gives us a smooth gradient on the leds. Guassian blur.
    x = x*6/100-3
    e=2.718281828459
    sqrt2pi_inv = 1/(3.1415*2)**0.5
    normal = sqrt2pi_inv*e**(-0.5*x**2)
    return normal * 1.25

def swirl(r_speed=20, h_speed = 0.01):
    # rotation
    offset = 0

    led_indexes = list(range(N_LEDS))
    hue = 0.5
    while True:
        # Calculate lightnesses with a nice gaussian distribution
        lightnesses = [gauss1((i*150/N_LEDS+offset)%150) for i in led_indexes]
        # Calculate rgb value with the current hue
        leds = [hsl_to_rgb(hue,1,l) for l in lightnesses]
        # Create a flat list of all color values in GRB format to write into the pixel buffer
        grb_flat = []
        for (r,g,b) in leds:
            grb_flat += [g,r,b]
        # write the complete neopixel buffer at once
        command="""np.buf = {}""".format(bytearray(grb_flat))
        wifi.execute(command)
        wifi.execute("np.write()")
        # increase rotation of image
        offset += r_speed
        # shift hue of 'image'
        hue += h_speed
        if hue > 1: hue = 0

# swirl()

def led_follow_mb(h_speed = 0.01):
    # rotation
    offset = 0

    led_indexes = list(range(N_LEDS))
    hue = 0.5
    while True:
        # Calculate lightnesses with a nice gaussian distribution
        lightnesses = [gauss1((i*200/N_LEDS+offset)%200) for i in led_indexes]
        # Calculate rgb value with the current hue
        leds = [hsl_to_rgb(hue,1,l) for l in lightnesses]
        # Create a flat list of all color values in GRB format to write into the pixel buffer
        grb_flat = []
        for (r,g,b) in leds:
            grb_flat += [g,r,b]
        # write the complete neopixel buffer at once
        command="""np.buf = {}""".format(bytearray(grb_flat))
        wifi.execute(command)
        wifi.execute("np.write()")
        # Change rotation of image
        offset = mb.get()[1]*-1
        # shift hue of 'image'
        hue += h_speed
        if hue > 1: hue = 0

led_follow_mb()