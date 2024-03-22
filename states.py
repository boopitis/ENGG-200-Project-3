from ili9341 import Display, color565
from hcsr04 import HCSR04

class Base_State:
    def __init__(self, lcd_display: Display):
        self.lcd_display = lcd_display
        self.movement_speed_factor = 1

    def idle(self, face_ascii: str):
        self.lcd_display.draw_image(face_ascii)
        print(face_ascii)
        # move calmly

    def greeting(self, face_image_path: str):
        self.lcd_display.draw_image(face_image_path)

    def response(self, face_image_path: str):
        self.lcd_display.draw_image(face_image_path)

    def annoyed(self, face_image_path: str):
        self.lcd_display.draw_image(face_image_path)

class Warm_Up(Base_State):
    def __init__(self, lcd_display: Display):
        super().__init__(lcd_display)
        self.movement_speed_factor = 1.2

    def idle(self, face_image_path:str):
        self.lcd_display.draw_image(face_image_path)
        # move energeticly

    def exercise(self, face_image_path:str, exercise_type):
        self.lcd_display.draw_image(face_image_path)

        # TODO: Implement exercise class
        # exercise_type.execute()

class Workout(Warm_Up):
    def __init__(self, lcd_display: Display):
        super().__init__(lcd_display)