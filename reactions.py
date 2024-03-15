from ili9341 import Display, color565

class Reaction:
    def idle(self, lcd_display: Display, ultrasonic_sensor):
        lcd_display.draw_image()