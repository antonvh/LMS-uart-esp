# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the rotary encoder module
# ESP8266/ESP32 implementation

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from machine import Pin
#from rotary import Rotary
from sys import platform

_esp8266_deny_pins = [16]


states=[[0,-1,1,0],[1,0,0,-1],[-1,0,0,1],[0,1,-1,0]]

import time




def _wrap(value, incr, lower_bound, upper_bound):
    range = upper_bound - lower_bound + 1
    value = value + incr

    if value < lower_bound:
        value += range * ((lower_bound - value) // range + 1)

    return lower_bound + (value - lower_bound) % range


def _bound(value, incr, lower_bound, upper_bound):
    return min(upper_bound, max(lower_bound, value + incr))


def _trigger(rotary_instance):
    for listener in rotary_instance._listener:
        listener()


class RotaryGen(object):

    #RANGE_UNBOUNDED = const(1)
    RANGE_WRAP = const(2)
    RANGE_BOUNDED = const(3)

    def __init__(self, min_val, max_val, reverse, range_mode):
        self._min_val = min_val
        self._max_val = max_val
        self._reverse = -1 if reverse else 1
        self._range_mode = range_mode
        self._value = min_val
        self._state = 0
        self._listener = []

    def set(self, value=None, min_val=None,
            max_val=None, reverse=None, range_mode=None):
        # disable DT and CLK pin interrupts
        self._hal_disable_irq()

        if value is not None:
            self._value = value
        else:
            self._value=0
        if min_val is not None:
            self._min_val = min_val
        if max_val is not None:
            self._max_val = max_val
        if reverse is not None:
            self._reverse = -1 if reverse else 1
        if range_mode is not None:
            self._range_mode = range_mode
        self._state = 0

        # enable DT and CLK pin interrupts
        self._hal_enable_irq()

    def value(self):
        return self._value

    def reset(self):
        self._value = 0

    def close(self):
        self._hal_close()

    def add_listener(self, l):
        self._listener.append(l)

    def remove_listener(self, l):
        if l not in self._listener:
            raise ValueError('{} is not an installed listener'.format(l))
        self._listener.remove(l)
        
    def _process_rotary_pins(self, pin):
        incr=0
        old_value = self._value
        old_state = self._state
        new_state=(self._get_bit_A() <<1) | self._get_bit_B()
        if old_state!=new_state:
            incr=states[old_state][new_state]*self._reverse
            self._state=new_state

        if self._range_mode == self.RANGE_WRAP:
            self._value = _wrap(
                self._value,
                incr,
                self._min_val,
                self._max_val)
        elif self._range_mode == self.RANGE_BOUNDED:
            self._value = _bound(
                self._value,
                incr,
                self._min_val,
                self._max_val)
        else:
            self._value = self._value + incr

        try:
            if old_value != self._value and len(self._listener) != 0:
                micropython.schedule(_trigger, self)
        except:
            pass


class Rotary(RotaryGen):
    RANGE_UNBOUNDED = const(1)
    def __init__(self, pin_num_A, pin_num_B, min_val=0, max_val=10,
                 reverse=False, range_mode=RANGE_UNBOUNDED, pull_up=False):

        if platform == 'esp8266':
            if pin_num_A in _esp8266_deny_pins:
                raise ValueError(
                    '%s: Pin %d not allowed. Not Available for Interrupt: %s' %
                    (platform, pin_num_A, _esp8266_deny_pins))
            if pin_num_B in _esp8266_deny_pins:
                raise ValueError(
                    '%s: Pin %d not allowed. Not Available for Interrupt: %s' %
                    (platform, pin_num_B, _esp8266_deny_pins))

        super().__init__(min_val, max_val, reverse, range_mode)

        if pull_up == True:
            self._pin_A = Pin(pin_num_A, Pin.IN, Pin.PULL_UP)
            self._pin_B = Pin(pin_num_B, Pin.IN, Pin.PULL_UP)
        else:
            self._pin_A = Pin(pin_num_A, Pin.IN)
            self._pin_B = Pin(pin_num_B, Pin.IN)

        self._enable_A_irq(self._process_rotary_pins)
        self._enable_B_irq(self._process_rotary_pins)

    def _enable_A_irq(self, callback=None):
        self._pin_A.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
            handler=callback)

    def _enable_B_irq(self, callback=None):
        self._pin_B.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
            handler=callback)

    def _disable_A_irq(self):
        self._pin_A.irq(handler=None)

    def _disable_B_irq(self):
        self._pin_B.irq(handler=None)

    def _get_bit_A(self):
        return self._pin_A.value()

    def _get_bit_B(self):
        return self._pin_B.value()

    def _hal_enable_irq(self):
        self._enable_A_irq(self._process_rotary_pins)
        self._enable_B_irq(self._process_rotary_pins)

    def _hal_disable_irq(self):
        self._disable_A_irq()
        self._disable_B_irq()

    def _hal_close(self):
        self._hal_disable_irq()
