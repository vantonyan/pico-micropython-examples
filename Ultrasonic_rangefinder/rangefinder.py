import machine, time
from machine import Pin
import math


class HCSR04:
    """
    Module used for range finder that has trigger and echo pins
    Used portions of the code from https://github.com/rsc1975/micropython-hcsr04
    """
    def __init__(self, trigger_pin, echo_pin, echo_timeout_mm, offset):
        self.echo_timeout_us = int(2*echo_timeout_mm / 0.34320)
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)
        
        # Offset error
        self.offset = offset

    def get_distance_mm(self):
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        # Get pulse from unit
        #print(self.echo_timeout_us)
        pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
        # print(pulse_time)
        if pulse_time == -1:
            print("Timeout: pulse is longer than limit")
            return 0
        elif pulse_time == -2:
            print("Timeout on waiting for a pulse")           
            print(self.echo_timeout_us)
            return 0
        
        # calculate distance in mm
        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        return math.ceil(0.34320 * (pulse_time/2)) + self.offset
        

rfinder = HCSR04(1, 0, 500, 17)
while True:
    dist = rfinder.get_distance_mm()
    #print("Distance %d" % dist)
    print(dist)
    time.sleep(1)
