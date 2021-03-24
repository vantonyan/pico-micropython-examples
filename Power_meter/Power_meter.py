from machine import Pin, I2C
from struct import unpack
from time import sleep
import utime
import math

global SHUNT_OHMS

SHUNT_OHMS = 0.1

ina_i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000) 
#ina_i2c.scan()

class ina219:
    REG_CONFIG = 0x00
    REG_SHUNTVOLTAGE = 0x01
    REG_BUSVOLTAGE = 0x02
    REG_POWER = 0x03
    REG_CURRENT = 0x04
    REG_CALIBRATION = 0x05
    
    def __init__(self,sr, address, maxi):
        self.address = address
        self.shunt = sr
            
    def vshunt(icur):
        global SHUNT_OHMS
        # Read Shunt register 1, 2 bytes
        reg_bytes = ina_i2c.readfrom_mem(icur.address, icur.REG_SHUNTVOLTAGE, 2)
        reg_value = int.from_bytes(reg_bytes, 'big')
        print(reg_value)
        if reg_value > 2**15: #negative
            for i in range(16): 
                reg_value = (reg_value ^ (1 << i))
        print(reg_value)
        return (float(reg_value) * 1e-4)
        #return reg_value
        
    def vbus(ivolt):
        reg_bytes = ina_i2c.readfrom_mem(ivolt.address, ivolt.REG_BUSVOLTAGE, 2)
        reg_value = int.from_bytes(reg_bytes, 'big') >> 3
        return float(reg_value) * 0.004
        
    def configure(conf):
        #ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x01\x9F') # PG = 1
        ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x09\x9F') # PG = /2
        ina_i2c.writeto_mem(conf.address, conf.REG_CALIBRATION, b'\x00\x00')

        

# Create current measuring object
ina = ina219(SHUNT_OHMS, 64, 5)
ina.configure()
utime.sleep_ms(10)

while True:
    v = ina.vbus()
    utime.sleep_ms(10) # Delay to avoid micropython error
    i = ina.vshunt()
    utime.sleep_ms(10) # Delay to avoid micropython error
    p = i * v
    print("v = %.2f" % v ,", i = %.2f" % i , ", P = %.2f" % p)
    sleep(1)