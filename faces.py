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
    
    def __init__(self, color=color565(0,0,0)):
        self.color = color

    def happy(self):
        lcd_display.fill_hrect(0, 0, 240, 320, color565(255,255,255))
        lcd_display.fill_vrect(80, 40, 30, 100, self.color)
        lcd_display.fill_vrect(85, 70, 20, 40, self.color)
        lcd_display.fill_vrect(85, 45, 20, 90, color565(255,255,255))
        lcd_display.fill_vrect(80 ,180 ,30, 100, self.color)
        lcd_display.fill_vrect(85, 185, 20, 90, color565(255,255,255))

if __name__ == "__main__":
    f = Faces(color565(0,0,0))
    f.happy()