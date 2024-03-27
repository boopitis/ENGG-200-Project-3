from ili9341 import Display, color565
from hcsr04 import HCSR04

class Base_State:
    def __init__(self, lcd_display: Display):
        self.lcd_display = lcd_display
        self.movement_speed_factor = 1

    def idle(self):
        #TODO: put this back self.lcd_display.draw_image(face_ascii)
        print('Idle action activated')
        # move calmly

    def greeting(self):
        #self.lcd_display.draw_image("ヾ(≧▽≦*)o")
        print("Greeting action activated")

    def response(self, face_ascii: str):
        self.lcd_display.draw_image(face_ascii)

    def annoyed(self, face_ascii: str):
        self.lcd_display.draw_image(face_ascii)

class Workout(Base_State):
    def __init__(self, lcd_display: Display):
        super().__init__(lcd_display)
        self.movement_speed_factor = 1.2

    def idle(self):
        #TODO: put this back self.lcd_display.draw_image(face_ascii)
        print('╚(•⌂•)╝')
        # move energeticly