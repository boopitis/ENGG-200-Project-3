"""ILI9341 demo (shapes)."""
import time
from ili9341 import Display, color565
from machine import Pin, SPI, ADC
from xglcd_font import XglcdFont
import utility

# Sample code from https://github.com/rdagger/micropython-ili9341/blob/master/demo_shapes.py

# Initialize Potentiometer
adc = ADC(Pin(26))
pot_max = 65535
pot_min = 208
pot_diff = pot_max - pot_min

# Initialize LCD Display
spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7))
display.clear()

selection = utility.menu()
print(selection)

sleep(5)
display.cleanup()
