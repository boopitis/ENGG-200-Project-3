print('i')

from machine import I2C, Pin, SPI, ADC
from imu import MPU6050
from neopixel import Neopixel
import tm1637
from ili9341 import Display, color565
import sdcard
import os
from hcsr04 import HCSR04
import utility
import time

print('i')

# Initialize Segment Display
tm = tm1637.TM1637(clk=Pin(20), dio=Pin(19))

# Initialize Gyroscope/Accelerometer
# i2c = I2C(1, scl=Pin(27), sda=Pin(26))
# imu = MPU6050(i2c)

# Initialize Ring Light
numpix = 8
strip = Neopixel(numpix, 1, 21, "GRB")
# strip = Neopixel(numpix, 0, 0, "GRBW")
strip.brightness(10)

# Initialize SD card
spi=SPI(0,baudrate=40000000,sck=Pin(2),mosi=Pin(3),miso=Pin(4))
sd=sdcard.SDCard(spi,Pin(5))
vfs=os.VfsFat(sd)
os.mount(sd,'/sd')
print(os.listdir('/sd'))

# Initialize LCD Display
spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7))
display.clear()

# Initialize Ultrasonic Sensor
sensor = HCSR04(trigger_pin=0, echo_pin=1)
distance = sensor.distance_cm()

# Initialize Potentiometer
adc = ADC(Pin(26))
pot_max = 65535
pot_min = 208
pot_diff = pot_max - pot_min

# Initialize Microphone
soundSensor = ADC(28) # Pin where sensor device (Microphone) is connected
led = Pin('LED', Pin.OUT)
baseline = 29000 # You may need to change this, but your mic should be reading around here as a baseline. 
variability = 0.1 # By being more selective about what we conside a spike, we can filter out noise. 10% is a good base level for a quiet room. 

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

tm.show('0420', True)

while True:
    strip.rotate_right(1)
    time.sleep(0.1)
    strip.show()
    
    try:
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
    except OSError as ex:
        print('ERROR getting distance:', ex)
        
    # If we detect a spike in the waveform greater than a 10% deviation from our baseline, someone is probably talking.
    if soundSensor.read_u16() > (baseline + baseline*variability) or soundSensor.read_u16() < (baseline - baseline*variability):
        led.on() # Turn the light on if we're detecting a spike
    else:
        led.off() # Otherwise, keep the light off
    
#     # print all values
#     print('Accelerometer',(imu.accel.xyz))
#     print('Gyroscope',(imu.gyro.xyz))
#     print('Temperature',(imu.temperature))
# 
#     #print a single value, e.g. x value of acceleration
#     print(imu.accel.x)
#     time.sleep(1)