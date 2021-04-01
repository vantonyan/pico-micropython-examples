from machine import Pin, I2C
from struct import unpack
from time import sleep
import utime
import math

MPU6050_i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000) 
#MPU6050_i2c.scan()
STANDARD_GRAVITY = 9.80665


class MPU6050:
    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    bus = None

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    ACCEL_XOUT0 = 0x3B
    ACCEL_YOUT0 = 0x3D
    ACCEL_ZOUT0 = 0x3F

    TEMP_OUT0 = 0x41

    GYRO_XOUT0 = 0x43
    GYRO_YOUT0 = 0x45
    GYRO_ZOUT0 = 0x47

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self,address):
        self.address = address

    def configure(conf):
        # Wake up the part
        MPU6050_i2c.writeto_mem(conf.address, conf.PWR_MGMT_1, b'\x00')
        MPU6050_i2c.writeto_mem(conf.address, conf.ACCEL_CONFIG, b'\x00')
        MPU6050_i2c.writeto_mem(conf.address, conf.GYRO_CONFIG, b'\x00')
        
    def twoes_int(self,reg_value):
        sign = 1
        if reg_value > 2**15: # negative current direction
            sign = -1
            for i in range(16): 
                reg_value = (reg_value ^ (1 << i))
        return reg_value * sign
    
    def get_temperature(gtemp):
        reg_bytes = MPU6050_i2c.readfrom_mem(gtemp.address, gtemp.MPU6050_TEMP_OUT,2 )
        reg_value = int.from_bytes(reg_bytes, 'big')
        return float(reg_value/ 340.0) + 25.53

    def get_accel_data(self, g = False):
        reg_bytes = MPU6050_i2c.readfrom_mem(self.address, self.ACCEL_XOUT0,2 )
        x = self.twoes_int(int.from_bytes(reg_bytes, 'big'))
        reg_bytes = MPU6050_i2c.readfrom_mem(self.address, self.ACCEL_YOUT0,2 )
        y = self.twoes_int(int.from_bytes(reg_bytes, 'big'))
        reg_bytes = MPU6050_i2c.readfrom_mem(self.address, self.ACCEL_ZOUT0,2 )
        z = self.twoes_int(int.from_bytes(reg_bytes, 'big'))
        
        accel_scale_modifier = None
        accel_range = int.from_bytes(MPU6050_i2c.readfrom_mem(self.address, self.ACCEL_CONFIG,1), 'big')

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
 
        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        
        x = x * self.GRAVITIY_MS2
        y = y * self.GRAVITIY_MS2
        z = z * self.GRAVITIY_MS2
        
        # Calculate angle and convert to degrees
        ax = math.atan2(x,z)*180/3.14
        ay = math.atan2(y,z)*180/3.14
        return {'ax': ax, "ay": ay}


    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope.

        Returns the read values in a dictionary.
        """
        reg_bytes = MPU6050_i2c.readfrom_mem(self.address, self.GYRO_XOUT0,2 )
        x = self.twoes_int(int.from_bytes(reg_bytes, 'big'))        
        reg_bytes = MPU6050_i2c.readfrom_mem(self.address, self.GYRO_YOUT0,2 )
        y = self.twoes_int(int.from_bytes(reg_bytes, 'big'))
        reg_bytes = MPU6050_i2c.readfrom_mem(self.address, self.GYRO_ZOUT0,2 )
        z = self.twoes_int(int.from_bytes(reg_bytes, 'big'))
        
        gyro_scale_modifier = None
        gyro_range = int.from_bytes(MPU6050_i2c.readfrom_mem(self.address, self.GYRO_CONFIG,1), 'big')

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier        
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}
        

        
# Create current measuring object
GYRO = MPU6050(104)
GYRO.configure()
utime.sleep_ms(10)

while True:
    print(GYRO.get_accel_data())
    utime.sleep_ms(500)
