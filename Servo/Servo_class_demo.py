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
        #self.a = 0
        
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
        
servo1 = my_servo(50,15,8000, 5000)
 
while True:
    for a in range(0, 90, 1):
        servo1.angle(a)
        sleep(0.1)
    sleep(1)
    
    for a in range(0, -90, -1):
        servo1.angle(a)
        sleep(0.1)
    sleep(1)
