# Work in progress
# Trying to make a rotating blob of leds that is shifting its hue.
# This code works on the esp.

from utime import sleep_ms
import machine

N_LEDS = 12

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
    x = x*6/100-3
    e=2.718281828459
    sqrt2pi_inv = 1/(3.1415*2)**0.5
    normal = sqrt2pi_inv*e**(-0.5*x**2)
    return normal * 1.25

def swirl(r_speed=1, h_speed = 0.01):
    offset = 0

    led_indexes = list(range(N_LEDS))

    hue = 0.5

    import neopixel
    np = neopixel.NeoPixel(machine.Pin(4),12)
    while True:
        lightnesses = [gauss1((i*100/N_LEDS+offset)%100) for i in led_indexes]
        leds = [hsl_to_rgb(hue,1,l) for l in lightnesses]
        for i in range(12): np[i]=leds[i]
        np.write()
        offset += r_speed
        hue += h_speed
        if hue > 1: hue = 0

swirl()