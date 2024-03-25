from machine import I2C, Pin, SPI, ADC, PWM
from imu import MPU6050
from neopixel import Neopixel
from ili9341 import Display, color565
from hcsr04 import HCSR04
from xglcd_font import XglcdFont
from wavePlayer import wavePlayer
from servo import Servo
from component_classes import Components
import time, os, sdcard, tm1637

components = Components(
    speaker_left_pin = 10,
    speaker_right_pin = 11,
    segment_display_clk_pin = 20,
    segment_display_dio_pin = 19,
    ring_light_pin = 21,
    sd_sck_pin = 2,
    sd_mosi_pin = 3,
    sd_miso_pin = 4,
    sd_pin = 5,
    lcd_sck_pin = 14,
    lcd_mosi_pin = 15,
    lcd_dc_pin = 6,
    lcd_cs_pin = 17,
    lcd_rst_pin = 7,
    ultrasonic_trigger_pin = 0,
    ultrasonic_echo_pin = 1,
    potentiometer_pin = 26,
    microphone_pin = 28,
    servo_pin = 18,
    button_pin = 22,
)

# Initialize Components ---------------------------------
player = components.speaker()
segment_display = components.segment_display()
segment_display.show('0000')

# sd = components.sd_card()
lcd_display = components.lcd_display()
font = XglcdFont('TimesNR28x25.h', 28, 25)

number_of_leds = 8
ring_light = components.ring_light(default_brightness=10, number_of_leds=number_of_leds)

button = components.button(is_PULL_DOWN=True)

class Exercise:
    def __init__(self, name):
        self.name = name
        
    def timed_exercise(self, duration=60):
        image = '/sd/' + self.name + '.raw'
        
        lcd_display.draw_image(image, 0, 0, 240, 320)
    
        player.play('/sd/get_ready.wav')
        time.sleep(2)
        ring_light.fill((255,0,0))
        ring_light.show()
        player.play('/sd/three.wav')
        time.sleep(1)
        player.play('/sd/two.wav')
        time.sleep(1)
        ring_light.fill((255,100,0))
        ring_light.show()
        player.play('/sd/one.wav')
        time.sleep(1)
        ring_light.fill((0,255,0))
        ring_light.show()
        player.play('/sd/go.wav')
        
        timer = duration
        
        while True:
            if button.value():
                break
            
            minutes = timer // 60
            seconds = timer - minutes * 60
            segment_display.numbers(minutes, seconds)
            
            if timer > 0:
                tenths += 1
                if (tenths == 10):    
                    timer -= 1
                    tenths = 0
            if (timer == 14 and tenths == 0):
                player.play('/sd/15_left.wav')
                
        ring_light.fill(red)
        ring_light.show()
        player.play('/sd/good_work.wav')
        
    def rep_exercise(self):
        image = '/sd/' + self.name + '.raw'
        
        lcd_display.draw_image(image, 0, 0, 240, 320)
    
        player.play('/sd/get_ready.wav')
        time.sleep(2)
        ring_light.fill((255,0,0))
        ring_light.show()
        player.play('/sd/three.wav')
        time.sleep(1)
        player.play('/sd/two.wav')
        time.sleep(1)
        ring_light.fill((255,100,0))
        ring_light.show()
        player.play('/sd/one.wav')
        time.sleep(1)
        ring_light.fill((0,255,0))
        ring_light.show()
        player.play('/sd/go.wav')
        
        while True:
            if button.value():
                break
                
        ring_light.fill(red)
        ring_light.show()
        player.play('/sd/good_work.wav')
