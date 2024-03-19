from ili9341 import Display, color565
from hcsr04 import HCSR04

class Reactions:
    def __init__(self, lcd_display: Display, ultrasonic_sensor: HCSR04) -> None:
        self.lcd_display = lcd_display
        self.ultrasonic_sensor = ultrasonic_sensor
        self.movement_speed_factor = 1

    def idle(self, face_image: str):
        self.lcd_display.draw_image(face_image)
        # move calmly

    def greeting(self, face_image: str):
        self.lcd_display.draw_image(face_image)

    def response(self, face_image: str):
        self.lcd_display.draw_image(face_image)

    def annoyed(self, face_image: str):
        self.lcd_display.draw_image(face_image)

class Warm_Up_Reactions(Reactions):
    def __init__(self, lcd_display: Display, ultrasonic_sensor: HCSR04) -> None:
        super().__init__(lcd_display, ultrasonic_sensor)
        self.movement_speed_factor = 1.2

    def idle(self, face_image:str):
        self.lcd_display.draw_image(face_image)
        # move energeticly