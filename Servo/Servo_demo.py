from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(15))
servo.freq(50)

# Mid position is 5000
# 90 degree is 2000
#-90 degre is 8000

# Set servo into 0 position 
servo.duty_u16(5000)


while True:
    for duty in range(5000, 6500, 100):
        servo.duty_u16(duty)
        sleep(0.1)
    sleep(1)
    
    for duty in range(5000, 3500, -100):
        servo.duty_u16(duty)
        sleep(0.1)
    sleep(1)
