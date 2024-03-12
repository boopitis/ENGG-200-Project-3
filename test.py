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

def menu():
    cur_option = 0
    options = ('Temperature', 'Wind Speed', 'Weather Code', 'Change Lat/Long','Brightness', 'Update', 'Power Off', '')
    num_options = len(options) - 1
    
    while True:
        time.sleep(0.1)
        option = round((adc.read_u16() - pot_min) / pot_diff * (num_options - 1)) + 1
        
        # print(adc.read_u16())
        if option != cur_option:
            display.clear()
            utility.draw_text2(5, 5, f'>{options[option - 1]}')
            utility.draw_text2(5, 30, f'{options[option]}')
        
#         if button.value() == 0:
#             return option
        
        cur_option = option

selection = menu()
print(selection)

sleep(5)
display.cleanup()
