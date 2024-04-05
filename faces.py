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

    def idle(self, thick=False):
        white = color565(255,255,255)
        lcd_display.fill_hrect(0, 0, 240, 320, white)

        # Eyes
        self.draw_rect(40, 80, 100, 30)
        self.draw_rect(45, 85, 90, 20, white)
        self.draw_rect(70, 85, 40, 20)
        self.draw_rect(180, 80, 100, 30)
        self.draw_rect(185, 85, 90, 20, white)
        self.draw_rect(210, 85, 40, 20)


        # Eyebrows
        if thick:
            self.draw_rect(40, 60, 100, 10)
            self.draw_rect(180, 60, 100, 10)
            lcd_display.draw_lines([[60, 320 - 30], [50, 320 -  40], [45, 320 - 60]], self.color)
            lcd_display.draw_lines([[60, 30], [50, 40], [45, 60]], self.color)
        else:
            self.draw_ellipse(80, 60, 60, 10)
            self.draw_ellipse(80, 60, 55, 5, white)
            self.draw_ellipse(240, 60, 60, 10)
            self.draw_ellipse(240, 60, 55, 5, white)
            self.draw_rect(20, 60, 280, 15, white)
            self.draw_rect(55, 50, 210, 5)
            self.draw_rect(130, 50, 60, 20, white)

        # Mouth
        self.draw_ellipse(220, 180, 30, 20)
        self.draw_ellipse(210, 161, 40, 30, white)
        self.draw_rect(90, 190, 130, 12)
        self.draw_rect(90, 180, 5, 30)
        lcd_display.draw_lines([[160,320 - 30], [180, 320 - 50], [220, 320 - 60]], self.color)
        lcd_display.draw_lines([[160,30], [180, 50], [220, 60]], self.color)
    
    def creep(self):
        white = color565(255,255,255)
        lcd_display.fill_hrect(0, 0, 240, 320, white)

        # Eyes
        self.draw_rect(40, 80, 100, 30)
        self.draw_rect(45, 85, 90, 20, white)
        self.draw_rect(70, 85, 40, 20)
        self.draw_rect(180, 80, 100, 30)
        self.draw_rect(185, 85, 90, 20, white)
        self.draw_rect(210, 85, 40, 20)

        # Eyebrows
        self.draw_rect(40, 60, 100, 10)
        self.draw_rect(180, 60, 100, 10)
        lcd_display.draw_lines([[60, 320 - 30], [50, 320 -  40], [45, 320 - 60]], self.color)
        lcd_display.draw_lines([[60, 30], [50, 40], [45, 60]], self.color)

        # Mouth
        self.draw_ellipse(160, 160, 100, 40)
        self.draw_ellipse(160, 160, 80, 30, white)
        self.draw_rect(60, 120, 200, 40, white)

    def happy(self):
        white = color565(255,255,255)
        lcd_display.fill_hrect(0, 0, 240, 320, white)

        # Eyes
        self.draw_ellipse(90, 100, 50, 10)
        self.draw_ellipse(90, 100, 45, 5, white)
        self.draw_ellipse(230, 100, 50, 10)
        self.draw_ellipse(230, 100, 45, 5, white)
        self.draw_rect(40, 100, 240, 15, white)

        # Eyebrows
        self.draw_ellipse(80, 60, 60, 10)
        self.draw_ellipse(80, 60, 55, 5, white)
        self.draw_ellipse(240, 60, 60, 10)
        self.draw_ellipse(240, 60, 55, 5, white)
        self.draw_rect(20, 60, 280, 15, white)
        self.draw_rect(55, 50, 210, 5)
        self.draw_rect(130, 50, 60, 20, white)

        # Mouth
        self.draw_ellipse(160, 160, 100, 40)
        self.draw_ellipse(160, 160, 90, 35, white)
        self.draw_rect(60, 120, 200, 40, white)
        self.draw_rect(60, 160, 200, 5)
        lcd_display.draw_lines([[160,320 - 30], [180, 320 - 50], [220, 320 - 60]], self.color)
        lcd_display.draw_lines([[160,30], [180, 50], [220, 60]], self.color)

if __name__ == "__main__":
    f = Faces(color565(0,0,0))
    f.idle()
    time.sleep(3)
    f.idle(True)
    time.sleep(3)
    f.happy()
    time.sleep(3)
    f.creep()
