from ili9341 import Display, color565
from hcsr04 import HCSR04
import asyncio

from faces import Faces

faces = Faces()

class Base_State:
    def __init__(self, lcd_display: Display):
        self.lcd_display = lcd_display
        self.movement_speed_factor = 1
        
    async def idle(self):
        print('Idle action activated')

        # Makes face bob up-and-down.
        faces.idle()
        await asyncio.sleep(1)
        faces.idle(x_offset=-3)
        faces.idle(x_offset=-2)
        await asyncio.sleep(0.2)

    async def greeting(self):
        print("Greeting action activated")

        faces.happy()
        await asyncio.sleep(1)
        faces.idle()

    async def response(self):
        faces.happy()
        await asyncio.sleep(0.2)
        faces.idle()

    async def annoyed(self, face_ascii: str):
        self.lcd_display.draw_image(face_ascii)

class Workout(Base_State):
    def __init__(self, lcd_display: Display):
        super().__init__(lcd_display)
        self.movement_speed_factor = 1.2

    async def idle(self):
        print('Exercise Idle action activated')

        # Makes face bob up-and-down.
        faces.idle(thick=True)
        await asyncio.sleep(1)
        faces.idle(x_offset=-3, thick=True)
        faces.idle(x_offset=-2, thick=True)
        await asyncio.sleep(0.2)