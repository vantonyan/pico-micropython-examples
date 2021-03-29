from machine import Pin, PWM, Timer
from time import sleep
import utime


class hx711:
    def __init__(self):        
        # Clock selection based on gain and channel
        self.hx_clk_count = 25 # Clock pulses for channel A
        self.hx_dat = 0  # Data register read
        # calibration values specific to load cell
        # Those are example reading from load cell using 100g, 50g and 20g
        # reference weights
        #    Weight	0	50	100	20
        #            89272	142598	196045	110675
        #            89725	142252	195606	110870
        #            89715	142510	195512	110733
        #    Mean    89570	142453	195721	110759
        #    Scale per gram     1057.66	1061.51	1059.45
        
        self.hx_offset = 89570 # no force point representing no load
        self.hx_scale = 1059   # repreenting 1 Gram reading value

    def calibrate(soffset, offset, scale):
        soffset.hx_offset = offset
        soffset.hx_scale = scale
        
    def check_ready(self):
        if hx_sdat.value() == 1:
            # data is not ready, return old data
            utime.sleep_us(100)
            return 0
        else:
            return 1
    
    def power_down():
        hx_sclk.value(1)
        utime.sleep_us(100)
        
    def power_up():
        hx_sclk.value(0)
        utime.sleep_us(10)

    def reset():
        hx_sclk.value(1)
        utime.sleep_us(100)
        hx_sclk.value(0)
    
    def read(hxread, gain, channel):
        # Clock selection based on gain and channel
        if channel > 0:
            # Select Channel B for reading
            hxread.hx_clk_count = 26
        else:
            # Select channel A for reading 
            if gain > 64:
                hxread.hx_clk_count = 25
            else:
                hxread.hx_clk_count = 27
                
        # bit banging to read data
        hxread.hx_dat = 0
        for i in range(hxread.hx_clk_count):
            # Pulse clk for 1uS
            hx_sclk.value(1)
            utime.sleep_us(1)
            hx_sclk.value(0)

            # Read data pin MSB first
            if i < 24:
                hxread.hx_dat = hxread.hx_dat << 1
                if hx_sdat.value() == 1:
                    hxread.hx_dat = hxread.hx_dat + 1
            # Hold the clk low for timing
            utime.sleep_us(1)                        

        # Return the data value that is in twoes complement format
        if hxread.hx_dat > 2**23: 
            for i in range(24): 
                hxread.hx_dat = (hxread.hx_dat ^ (1 << i))
        
        return hxread.hx_dat

    def read_force(rforce):
        force = rforce.read_median(3)
        
        # Scale output
        force = (force - rforce.hx_offset) / rforce.hx_scale
        return force

    # A median-based read method, might help when getting random value spikes
    # for unknown or CPU-related reasons
    def read_median(self, times=3):
        if times <= 0:
            raise ValueError("HX711::read_median(): times must be greater than zero!")

        # If times == 1, just return a single reading.
        if times == 1:
            return self.read(64, 0)
            utime.sleep_ms(300)

        valueList = []
        for x in range(times):
            valueList += [self.read(64, 0)]
            utime.sleep_ms(200)
        
        valueList.sort()
        # If times is odd we can just take the centre value.
        if (times & 0x1) == 0x1:
            return valueList[len(valueList) // 2]
        else:
            # If times is even we have to take the arithmetic mean of
            # the two middle values.
            midpoint = len(valueList) / 2
        return sum(valueList[midpoint:midpoint+2]) / 2.0

# Assign pins to the controller
hx_sdat = Pin(0, Pin.IN, Pin.PULL_UP)
hx_sclk = Pin(1, Pin.OUT)

# create object for the sensor
hx711_object = hx711()

while True:
    reg_value = 0
    if hx711_object.check_ready() == 1:
        print("%.2f" % hx711_object.read_force())
        utime.sleep(1)

#         
