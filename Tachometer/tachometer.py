from machine import Pin, PWM, Timer
hall_sensor = Pin(15, Pin.IN, Pin.PULL_UP)
timer = Timer()
global count, hsense, hstate
count = 0
hsense = 0

def timer_event(timer):
    global count
    global hsense, hstate
    # hsense contains number of pulses (rotations) per second 
    if hall_sensor() == 0:
        if hstate == 1:
            hsense = hsense + 1
            hstate = 0
    else:
        hstate = 1
    if count == 1000 :
        # Print RPM of the tachometer
        print(hsense*60)
        hsense = 0
        count = 0
    else:
        count = count + 1 
    

timer.init(freq=1000, mode=Timer.PERIODIC, callback=timer_event)

# Construct PWM object, with LED on Pin(25).
onboard_LED = PWM(Pin(25))

# Set the PWM frequency.
onboard_LED.freq(1000)

while True:
    if hall_sensor() == 0:
        onboard_LED.duty_u16(30000)
    else:
        onboard_LED.duty_u16(0)
        