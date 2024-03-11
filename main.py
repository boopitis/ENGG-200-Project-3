from machine import I2C, Pin, SPI
from imu import MPU6050
from neopixel import Neopixel
import tm1637
from ili9341 import Display, color565
import sdcard
import os
import time

# Initialize Segment Display
tm = tm1637.TM1637(clk=Pin(14), dio=Pin(15))

# Initialize Gyroscope/Accelerometer
i2c = I2C(1, scl=Pin(27), sda=Pin(26))
imu = MPU6050(i2c)

# Initialize Ring Light
numpix = 8
strip = Neopixel(numpix, 1, 20, "GRB")
# strip = Neopixel(numpix, 0, 0, "GRBW")
strip.brightness(10)

# Initialize SD card
spi=SPI(0,baudrate=40000000,sck=Pin(2),mosi=Pin(3),miso=Pin(4))
sd=sdcard.SDCard(spi,Pin(5))

# Initialize LCD Display
spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7))
display.clear()

# Create a instance of MicroPython Unix-like Virtual File System (VFS),
vfs=os.VfsFat(sd)
 
# Mount the SD card
os.mount(sd,'/sd')

# Debug print SD card directory and files
print(os.listdir('/sd'))

red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

# same colors as normaln rgb, just 0 added at the end
colors_rgbw = [color+tuple([0]) for color in colors_rgb]
colors_rgbw.append((0, 0, 0, 255))

# uncomment colors_rgbw if you have RGBW strip
colors = colors_rgb
# colors = colors_rgbw

step = round(numpix / len(colors))
current_pixel = 0

for color1, color2 in zip(colors, colors[1:]):
    strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
    current_pixel += step

strip.set_pixel_line_gradient(current_pixel, numpix - 1, violet, red)

while True:
    strip.rotate_right(1)
    time.sleep(0.1)
    strip.show()
    
    # print all values
    print('Accelerometer',(imu.accel.xyz))
    print('Gyroscope',(imu.gyro.xyz))
    print('Temperature',(imu.temperature))

    #print a single value, e.g. x value of acceleration
    print(imu.accel.x)
    time.sleep(1)