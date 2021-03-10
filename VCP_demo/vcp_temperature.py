import machine
import utime
import _thread

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

def temperature_display_thread():
    while True:
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706)/0.001721
        temperature = (temperature* 1000 - (temperature * 1000) % 10)/1000
        print(str(temperature)+str(" C"))
        utime.sleep(1)

_thread.start_new_thread(temperature_display_thread, ())

from machine import Pin, PWM
# Construct PWM object, with LED on Pin(25).
pwm = PWM(Pin(25))

# Set the PWM frequency.
pwm.freq(1000)

# Fade the LED in and out a few times.
duty = 0
direction = 1
while True:
    for _ in range(8 * 256):
        duty += direction
        if duty > 255:
            duty = 255
            direction = -1
        elif duty < 0:
            duty = 0
            direction = 1
        pwm.duty_u16(duty * duty)
        utime.sleep(0.005)

