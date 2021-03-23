This project is built using hall effect sensor and magnet to detect the number of Rotations Per Minute (RPM). The hall effect sensor is available from Amazon (https://amzn.to/3sf8G7N  about \$5)and the magnets we use are available (https://amzn.to/396ur1K about \$12) 

The sensor is hooked up to the following pins on Raspberry Pico board:

- Hall effect sensor pin marked - : Pico board Pin 38 (GND)
- Hall effect sensor middle pin	: Pico board Pin 36 (3V3)
- Hall effect sensor pin marked S : Pico board Pin 20 (GP15)

After connecting the hall effect sensor to Pico board, connect the USB cable and open tachometer.py in Thonny and hit run button.

The shell will display the RPM of rotating object with attached magnet. To test the hardware you can move a magnet on an off the hall sensor. Onboard LED should light up when the magnet is close to hall effect sensor. Notice that the sensor only responds to North pole of the magnet

