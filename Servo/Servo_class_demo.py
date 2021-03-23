from machine import Pin, PWM
from time import sleep

class my_servo:
    def __init__(self,freq, pin, smax, smin):
        self.freq = freq
        self.pin = pin
        self.smax = smax #  90 degree position
        self.smid = smin #   0 degree position
        self.smin = self.smid - self.smax +self.smid   # -90 degree position
        self.servo_pwm = PWM(Pin(self.pin))
        self.servo_pwm.freq(self.freq)
        
    def angle(aset, a):
        #angle can be between -90 to 90
        if a >  90: a =  90
        if a < -90: a = -90
        # Calculate duty cycle
        aset.duty = int((aset.smax - aset.smid) / 90)
        if a > 0:
            aset.servo_pwm.duty_u16(aset.smid + aset.duty*a)
        elif a == 0:
            aset.servo_pwm.duty_u16(aset.smid)
        else:
            aset.servo_pwm.duty_u16(aset.smid + aset.duty*a)
    
    def calibrate(calib, csmax, csmin):
        # Calibrate 0 and 90 degree positions values
        calib.smax = csmax
        calib.smin = csmin

# Create servo controller with frequency of 50Hz, attached to pin GP15 and having
# Middle position of 5000 and maximum position at 9000
servo1 = my_servo(50,15,9000, 5000)

# Create second servo controller object attached to pin GP14
servo2 = my_servo(50,14,9000, 5000)

# Calibrate servo 0 and 90  degree angle
# You can set the angle to 0 degrees followd by 90 degrees and compare servo position
# with corner of payper sheet or post-it note
# servo1.angle(0)
# servo1.angle(90)
# servo1.calibrate(8000, 5000)
# Repeat above sequence until you are satisfied with results

while True:
    for a in range(0, 90, 1):
        servo1.angle(a)
        sleep(0.1)
    sleep(1)
    
    for a in range(0, -90, -1):
        servo1.angle(a)
        sleep(0.1)
    sleep(1)

