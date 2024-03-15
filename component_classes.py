from machine import I2C, Pin, SPI, ADC, PWM
from imu import MPU6050
from neopixel import Neopixel
import tm1637
from ili9341 import Display, color565
import sdcard
import os
from hcsr04 import HCSR04
from xglcd_font import XglcdFont
from wavePlayer import wavePlayer
from servo import Servo
import time

class Components:
    
    def __init__(self, speaker_left_pin=10, speaker_right_pin=11, segment_display_clk_pin=20, segment_display_dio_pin=19, 
                 ring_light_pin=21, sd_sck_pin=2, sd_mosi_pin=3, sd_miso_pin=4, sd_pin=5, lcd_sck_pin=14, lcd_mosi_pin=15, 
                 lcd_dc_pin=6, lcd_cs_pin=17, lcd_rst_pin=7, ultrasonic_trigger_pin=0, ultrasonic_echo_pin=1, potentiometer_pin=26, 
                 microphone_pin=28, servo_pin=18, button_pin=22):
        self.speaker_left_pin = speaker_left_pin
        self.speaker_right_pin = speaker_right_pin
        self.segment_display_clk_pin = segment_display_clk_pin
        self.segment_display_dio_pin = segment_display_dio_pin
        self.ring_light_pin = ring_light_pin
        self.sd_sck_pin = sd_sck_pin
        self.sd_mosi_pin = sd_mosi_pin
        self.sd_miso_pin = sd_miso_pin
        self.sd_pin = sd_pin
        self.lcd_sck_pin = lcd_sck_pin
        self.lcd_mosi_pin = lcd_mosi_pin
        self.lcd_dc_pin = lcd_dc_pin
        self.lcd_cs_pin = lcd_cs_pin
        self.lcd_rst_pin = lcd_rst_pin
        self.ultrasonic_trigger_pin = ultrasonic_trigger_pin
        self.ultrasonic_echo_pin = ultrasonic_echo_pin
        self.potentiometer_pin = potentiometer_pin
        self.microphone_pin = microphone_pin
        self.servo_pin = servo_pin
        self.button_pin = button_pin


    # Initialize Speaker
    def speaker(self):
        return wavePlayer(Pin(self.speaker_left_pin), Pin(self.speaker_right_pin))


    # Initialize Segment Display
    def segment_display(self):
        return tm1637.TM1637(clk=Pin(20), dio=Pin(19))

    # Initialize Ring Light
    def ring_light(self, default_brightness=10, number_of_leds=8):
        strip = Neopixel(number_of_leds, 1, self.ring_light_pin, "GRB")
        strip.brightness(default_brightness)

        return strip

    # Initialize SD card
    def sd_card(self, baudrate=40000000):
        spi=SPI(0,baudrate=baudrate,sck=Pin(self.sd_sck_pin),mosi=Pin(self.sd_mosi_pin),miso=Pin(self.sd_miso_pin))
        sd=sdcard.SDCard(spi,Pin(self.sd_pin))
        vfs=os.VfsFat(sd)
        os.mount(sd,'/sd')
        print(os.listdir('/sd'))

        return sd

    # Initialize LCD Display
    def lcd_display(self, baudrate=40000000):
        spi = SPI(1, baudrate=baudrate, sck=Pin(self.lcd_sck_pin), mosi=Pin(self.lcd_mosi_pin))
        display = Display(spi, dc=Pin(self.lcd_dc_pin), cs=Pin(self.lcd_cs_pin), rst=Pin(self.lcd_rst_pin))
        display.clear()

        return display

    # Initialize Ultrasonic Sensor
    def ultrasonic_sensor(self):
        return HCSR04(trigger_pin=self.ultrasonic_trigger_pin, echo_pin=self.ultrasonic_echo_pin)
            

    # Initialize Potentiometer
    def potentiometer(self) -> ADC:
        adc = ADC(Pin(self.potentiometer_pin))
        return adc

    # Initialize Microphone
    def microphone(self):
        return ADC(self.microphone_pin) # Pin where sensor device (Microphone) is connected
  

    # Initialize Servo
    def servo(self):
        return Servo(pin = self.servo_pin)

    # Initialize Button
    def button(self, is_PULL_DOWN=True):
        if is_PULL_DOWN:
            pin_type = Pin.PULL_DOWN
        else:
            pin_type = Pin.PULL_UP

        return Pin(self.button_pin, Pin.IN, pin_type)
        
    # Initialize Gyroscope/Accelerometer, 
    # TODO: Will need to add pins as parameters in the class.
    # i2c = I2C(1, scl=Pin(27), sda=Pin(26))
    # imu = MPU6050(i2c)