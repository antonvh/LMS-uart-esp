from uartremote import *
u=UartRemote(Port.S1)
mb=Motor(Port.A)



N_LEDS = 24

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
    u.send_receive('neoinit','B',N_LEDS)
    led_indexes = list(range(N_LEDS))
    hue = 0.5
    while True:
        # Calculate lightnesses with a nice gaussian distribution
        lightnesses = [gauss1((i*150/N_LEDS+offset)%150) for i in led_indexes]
        # Calculate rgb value with the current hue
        leds = [hsl_to_rgb(hue,1,l) for l in lightnesses]
        # Create a flat list of all color values in GRB format to write into the pixel buffer
        grb_flat = [0,N_LEDS]
        for (r,g,b) in leds:
            grb_flat += [g,r,b]
        # write the complete neopixel buffer at once
        #command="""np.buf = {}""".format(bytearray(grb_flat))
        q=u.send_receive('neosa','B',grb_flat)
        q=u.send_receive('neow')
        # increase rotation of image
        offset += r_speed
        print(offset)
        # shift hue of 'image'
        hue += h_speed
        if hue > 1: hue = 0

#swirl()

def led_follow_mb(h_speed = 0.01):
    # rotation
    offset = 0
    u.send_receive('neoinit','B',N_LEDS) # initialize neopixel leds

    led_indexes = list(range(N_LEDS))
    hue = 0.5
    while True:
        # Calculate lightnesses with a nice gaussian distribution
        lightnesses = [gauss1((i*200/N_LEDS+offset)%200) for i in led_indexes]
        # Calculate rgb value with the current hue
        leds = [hsl_to_rgb(hue,1,l) for l in lightnesses]
        # Create a flat list of all color values in GRB format to write into the pixel buffer
        grb_flat = [0,N_LEDS] # first element is first pixel, 2nd is number of pixels
        for (r,g,b) in leds:
            grb_flat += [g,r,b]
        # write the complete neopixel buffer at once
        q=u.send_receive('neosa','B',grb_flat) # set neopixels
        q=u.send_receive('neow') # call neopixel erite
        # Change rotation of image
        offset = mb.angle()   # get angle of Motor A
        print(offset)
        # shift hue of 'image'
        hue += h_speed
        if hue > 1: hue = 0

led_follow_mb()