This demo is quick and dirty update showing how to use virtual serial port on PC to display Raspberry pi Pico output.

Seems very basic but there is no much info on how to use VCP with micropython and it is very basic.

To use this program:

1. Use Thonny GUI to open this file
2. Then Save As to Rasberry Pi Pico with filename main.py
3. Close Thonny 
4. Disconnect the USB cable from Rasberry Pi Pico board and reconnect, forcing it to run main.py at power up
5. Use Teraterm on windows machine to open the Virtual Serial Port of Raspberry Pi Pico at baudrate of 115200 bits per second

The teraterm window will show temperature of RP2040 internal sensor every second. Also the onboard LED will fade in and out showing that program is running
Please note that most of the code is shamelessly copied from other example projects. I just got my board this morning and excellent example code and documentation helped me a lot.
