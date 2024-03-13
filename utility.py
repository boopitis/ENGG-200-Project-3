import time
from ili9341 import Display, color565
from machine import Pin, SPI, ADC
from xglcd_font import XglcdFont

# Initialize Potentiometer
adc = ADC(Pin(26))
pot_max = 65535

# Initialize LCD Display
spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7))

class Utility:
    def __init__(self, font):
        self.font = font
        
    def reversed_string(text):
        result = ""
        for char in text:
            result = char + result
            
        return result

    def draw_text2(x, y, text):
        display.draw_text(0 + y, 320 - x, reversed_string(text), font, color565(255,255,255), 0, True, True, 1)

    def menu():
        cur_option = 0
        options = ('Temperature', 'Wind Speed', 'Weather Code', 'Change Lat/Long','Brightness', 'Update', 'Power Off', '')
        num_options = len(options) - 1
        
        while True:
            time.sleep(0.1)
            option = round(adc.read_u16() / pot_max * (num_options - 1)) + 1
            
            print(adc.read_u16())
            if option != cur_option:
                display.clear()
                draw_text2(5, 5, f'>{options[option - 1]}')
                draw_text2(5, 30, f'{options[option]}')
            
    #         if button.value() == 0:
    #             return option
            
            cur_option = option
            
if __name__ == "__main__":
    print('i')