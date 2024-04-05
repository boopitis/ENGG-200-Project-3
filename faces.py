from machine import Pin
from ili9341 import Display, color565
from component_classes import Components
import time

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

    def draw_rect(self, x, y, w, h, color=color565(0,0,0)):
        """Draw a filled rectangle.
        Args:
            x (int): Starting X position.
            y (int): Starting Y position.
            w (int): Width of rectangle.
            h (int): Height of rectangle.
            color (int): RGB565 color value.
        """
        lcd_display.fill_vrect(y, 320 - x - w, h, w, color)

    def draw_ellipse(self, x, y, a, b, color=color565(0,0,0)):
        """Draw a filled ellipse.

        Args:
            x, y (int): Coordinates of center point.
            a (int): Semi axis horizontal.
            b (int): Semi axis vertical.
            color (int): RGB565 color value.
        Note:
            The center point is the center of the x0,y0 pixel.
            Since pixels are not divisible, the axes are integer rounded
            up to complete on a full pixel.  Therefore the major and
            minor axes are increased by 1.
        """

        lcd_display.fill_ellipse(y, 320 - x, b, a, color)

    def idle(self, thick=False, x_offset=0, y_offset=0):
        white = color565(255,255,255)
        lcd_display.fill_hrect(0 + x_offset, 0, 240, 320, white)

        # Eyes
        self.draw_rect(40 + x_offset, 80 + y_offset, 100, 30)
        self.draw_rect(45 + x_offset, 85 + y_offset, 90, 20, white)
        self.draw_rect(70 + x_offset, 85 + y_offset, 40, 20)
        self.draw_rect(180 + x_offset, 80 + y_offset, 100, 30)
        self.draw_rect(185 + x_offset, 85 + y_offset, 90, 20, white)
        self.draw_rect(210 + x_offset, 85 + y_offset, 40, 20)


        # Eyebrows
        if thick:
            self.draw_rect(40 + x_offset, 60 + y_offset, 100, 10)
            self.draw_rect(180 + x_offset, 60 + y_offset, 100, 10)
            lcd_display.draw_lines([[60 + x_offset, (320 - 30) + y_offset], [50 + x_offset, (320 - 40) + y_offset], [45 + x_offset, (320 - 60) + y_offset]], self.color)
            lcd_display.draw_lines([[60 + x_offset, 30 + y_offset], [50 + x_offset, 40 + y_offset], [45 + x_offset, 60 + y_offset]], self.color)
        else:
            self.draw_ellipse(80 + x_offset, 60 + y_offset, 60, 10)
            self.draw_ellipse(80 + x_offset, 60 + y_offset, 55, 5, white)
            self.draw_ellipse(240 + x_offset, 60 + y_offset, 60, 10)
            self.draw_ellipse(240 + x_offset, 60 + y_offset, 55, 5, white)
            self.draw_rect(20 + x_offset, 60 + y_offset, 280, 15, white)
            self.draw_rect(55 + x_offset, 50 + y_offset, 210, 5)
            self.draw_rect(130 + x_offset, 50 + y_offset, 60, 20, white)

        # Mouth
        self.draw_ellipse(220 + x_offset, 180 + y_offset, 30, 20)
        self.draw_ellipse(210 + x_offset, 161 + y_offset, 40, 30, white)
        self.draw_rect(90 + x_offset, 190 + y_offset, 130, 12)
        self.draw_rect(90 + x_offset, 180 + y_offset, 5, 30)
        lcd_display.draw_lines([[160 + x_offset, (320 - 30) + y_offset], 
                                [180 + x_offset, (320 - 50) + y_offset], 
                                [220 + x_offset, (320 - 60) + y_offset]], 
                                self.color)
        lcd_display.draw_lines([[160 + x_offset, 30 + y_offset], 
                                [180 + x_offset, 50 + y_offset], 
                                [220 + x_offset, 60 + y_offset]], 
                                self.color)
    
    def creep(self, x_offset=0, y_offset=0):
        white = color565(255,255,255)
        lcd_display.fill_hrect(0, 0, 240, 320, white)

        # Eyes
        self.draw_rect(40 + x_offset, 80 + y_offset, 100, 30)
        self.draw_rect(45 + x_offset, 85 + y_offset, 90, 20, white)
        self.draw_rect(70 + x_offset, 85 + y_offset, 40, 20)
        self.draw_rect(180 + x_offset, 80 + y_offset, 100, 30)
        self.draw_rect(185 + x_offset, 85 + y_offset, 90, 20, white)
        self.draw_rect(210 + x_offset, 85 + y_offset, 40, 20)

        # Eyebrows
        self.draw_rect(40 + x_offset, 60 + y_offset, 100, 10)
        self.draw_rect(180 + x_offset, 60 + y_offset, 100, 10)
        lcd_display.draw_lines([[60 + x_offset, (320 - 30) + y_offset], 
                                [50 + x_offset, (320 -  40) + y_offset], 
                                [45 + x_offset, (320 - 60) + y_offset]], 
                                self.color)
        lcd_display.draw_lines([[60 + x_offset, 30 + y_offset], 
                                [50 + x_offset, 40 + y_offset], 
                                [45 + x_offset, 60 + y_offset]], 
                                self.color)

        # Mouth
        self.draw_ellipse(160 + x_offset, 160 + y_offset, 100, 40)
        self.draw_ellipse(160 + x_offset, 160 + y_offset, 80, 30, white)
        self.draw_rect(60 + x_offset, 120 + y_offset, 200, 40, white)

    def happy(self, x_offset=0, y_offset=0):
        white = color565(255,255,255)
        lcd_display.fill_hrect(0, 0, 240, 320, white)

        # Eyes
        self.draw_ellipse(90 + x_offset, 100 + y_offset, 50, 10)
        self.draw_ellipse(90 + x_offset, 100 + y_offset, 45, 5, white)
        self.draw_ellipse(230 + x_offset, 100 + y_offset, 50, 10)
        self.draw_ellipse(230 + x_offset, 100 + y_offset, 45, 5, white)
        self.draw_rect(40 + x_offset, 100, 240 + y_offset, 15, white)

        # Eyebrows
        self.draw_ellipse(80 + x_offset, 60 + y_offset, 60, 10)
        self.draw_ellipse(80 + x_offset, 60 + y_offset, 55, 5, white)
        self.draw_ellipse(240 + x_offset, 60 + y_offset, 60, 10)
        self.draw_ellipse(240 + x_offset, 60 + y_offset, 55, 5, white)
        self.draw_rect(20 + x_offset, 60 + y_offset, 280, 15, white)
        self.draw_rect(55 + x_offset, 50 + y_offset, 210, 5)
        self.draw_rect(130 + x_offset, 50 + y_offset, 60, 20, white)

        # Mouth
        self.draw_ellipse(160 + x_offset, 160 + y_offset, 100, 40)
        self.draw_ellipse(160 + x_offset, 160 + y_offset, 90, 35, white)
        self.draw_rect(60 + x_offset, 120 + y_offset, 200, 40, white)
        self.draw_rect(60 + x_offset, 160 + y_offset, 200, 5)
        lcd_display.draw_lines([[160 + x_offset, (320 - 30) + y_offset], 
                                [180 + x_offset, (320 - 50) + y_offset], 
                                [220 + x_offset, (320 - 60) + y_offset]], 
                                self.color)
        lcd_display.draw_lines([[160 + x_offset, 30 + y_offset], 
                                [180 + x_offset, 50 + y_offset], 
                                [220 + x_offset, 60 + y_offset]], 
                                self.color)
        
    def blank(self):
        white = color565(255,255,255)
        lcd_display.fill_hrect(0, 0, 240, 320, white)

if __name__ == "__main__":
    f = Faces(color565(0,0,0))
    f.idle()
    time.sleep(3)
    f.idle(True)
    time.sleep(3)
    f.happy()
    time.sleep(3)
    f.creep()
