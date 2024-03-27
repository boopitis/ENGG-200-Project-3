from machine import Pin
from ili9341 import Display, color565
from component_classes import Components

components = Components(
    lcd_sck_pin = 14,
    lcd_mosi_pin = 15,
    lcd_dc_pin = 6,
    lcd_cs_pin = 17,
    lcd_rst_pin = 7,
)

# Initialize Components ---------------------------------
lcd_display = components.lcd_display()
# -------------------------------------------------------

class Faces():
    def __init__(self, colour=(0,0,0)):
        self.colour = colour

    def happy(self):
        