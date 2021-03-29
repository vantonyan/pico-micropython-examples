This example is using ina219 from TI to measure voltage and current over I2C
There are many boards available that already have ina219 installed with all supporting circuitry.
We used the INA219 modules are available from Amazon (https://amzn.to/31hzGaH) for this project

Sensor board connections are:

- INA219 VCC -> Pico pin 36
- INA219 GND -> Pico pin 38
- INA219 SCL -> Pico pin 2 (GP1)
- INA219 SDA -> Pico pin 1 (GP0)

The code displays current, voltage and power levels of the sensor board.
Using this setup one can easily calculate power consumption and even come up with algorithm to implement MPP (Maximum Power Point)regulation for solar panels etc.
