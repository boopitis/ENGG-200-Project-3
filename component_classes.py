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
    
    def __init__(self, speaker_left_pin=None, speaker_right_pin=None, segment_display_clk_pin=None, segment_display_dio_pin=None, 
                 ring_light_pin=None, sd_sck_pin=None, sd_mosi_pin=None, sd_miso_pin=None, sd_pin=None, lcd_sck_pin=None, lcd_mosi_pin=None, 
                 lcd_dc_pin=None, lcd_cs_pin=None, lcd_rst_pin=None, ultrasonic_trigger_pin=None, ultrasonic_echo_pin=None, potentiometer_pin=None, 
                 microphone_pin=None, servo_pin=None, button_pin=None):
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
        if self.speaker_left_pin != None and self.speaker_right_pin != None:
            return wavePlayer(Pin(self.speaker_left_pin), Pin(self.speaker_right_pin))
        else:
            raise ValueError("One of the Speaker pins has not been defined.")


    # Initialize Segment Display
    def segment_display(self):
        if self.segment_display_clk_pin != None and self.segment_display_dio_pin:
            return tm1637.TM1637(clk=Pin(20), dio=Pin(19))
        else:
            raise ValueError("One of the Segment Display pins has not been defined")

    # Initialize Ring Light
    def ring_light(self, default_brightness=10, number_of_leds=8):
        if self.ring_light_pin != None:
            strip = Neopixel(number_of_leds, 1, self.ring_light_pin, "GRB")
            strip.brightness(default_brightness)

            return strip
        else:
            raise ValueError("One of the Ring Light pins has not been defined")

    # Initialize SD card
    def sd_card(self, baudrate=40000000):
        if self.sd_sck_pin != None and self.sd_mosi_pin != None and self.sd_miso_pin != None and self.sd_pin != None:
            spi=SPI(0,baudrate=baudrate,sck=Pin(self.sd_sck_pin),mosi=Pin(self.sd_mosi_pin),miso=Pin(self.sd_miso_pin))
            sd=sdcard.SDCard(spi,Pin(self.sd_pin))
            vfs=os.VfsFat(sd)
            os.mount(sd,'/sd')
            print(os.listdir('/sd'))

            return sd
        else:
            raise ValueError("One of the SD card pins has not been defined")

    # Initialize LCD Display
    def lcd_display(self, baudrate=40000000):
        if self.lcd_sck_pin != None and self.lcd_mosi_pin != None and self.lcd_dc_pin != None and self.lcd_cs_pin != None and self.lcd_rst_pin != None:
            spi = SPI(1, baudrate=baudrate, sck=Pin(self.lcd_sck_pin), mosi=Pin(self.lcd_mosi_pin))
            display = Display(spi, dc=Pin(self.lcd_dc_pin), cs=Pin(self.lcd_cs_pin), rst=Pin(self.lcd_rst_pin))
            display.clear()

            return display
        else:
            raise ValueError("One of the LCD Display pins has not been defined")

    # Initialize Ultrasonic Sensor
    def ultrasonic_sensor(self):
        if self.ultrasonic_trigger_pin != None and self.ultrasonic_echo_pin != None:
            return HCSR04(trigger_pin=self.ultrasonic_trigger_pin, echo_pin=self.ultrasonic_echo_pin)
        else:
            raise ValueError("One of the Ultrasonic Sensor pins has not been defined")
            

    # Initialize Potentiometer
    def potentiometer(self):
        if self.potentiometer_pin != None:
            adc = ADC(Pin(self.potentiometer_pin))
            return adc
        else:
            raise ValueError("The Potentiometer pin has not been defined")

    # Initialize Microphone
    def microphone(self):
        if self.microphone_pin != None:
            return ADC(self.microphone_pin) # Pin where sensor device (Microphone) is connected
        else:
            raise ValueError("The Microphone pin has not been defined")
  

    # Initialize Servo
    def servo(self):
        if self.servo_pin != None:
            return Servo(pin = self.servo_pin)
        else:
            raise ValueError("The Servo pin has not been defined")

    # Initialize Button
    def button(self, is_PULL_DOWN=True):
        if self.button_pin != None:
            if is_PULL_DOWN:
                pin_type = Pin.PULL_DOWN
            else:
                pin_type = Pin.PULL_UP

            return Pin(self.button_pin, Pin.IN, pin_type)
        else:
            raise ValueError("The Button pin has not been defined")
        
    # Initialize Gyroscope/Accelerometer, 
    # TODO: Will need to add pins as parameters in the class.
    # i2c = I2C(1, scl=Pin(27), sda=Pin(26))
    # imu = MPU6050(i2c)