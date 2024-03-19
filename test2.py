from machine import Pin
import time

led = Pin('LED', Pin.OUT)
button = Pin(22, Pin.IN, Pin.PULL_DOWN)

while True:
    if button.value():
        led.toggle()
        print('boop')
        time.sleep(0.5)
