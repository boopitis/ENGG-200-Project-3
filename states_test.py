from machine import I2C, Pin, SPI, ADC, PWM
from servo import Servo
from xglcd_font import XglcdFont
import time, os, sdcard, tm1637

from component_classes import Components
from states import Base_State, Warm_Up, Workout

print('Initializing Components')

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
)

# Initialize Components ---------------------------------
player = components.speaker()
segment_display = components.segment_display()
segment_display.show('0000')

number_of_leds = 8
ring_light = components.ring_light(default_brightness=10, number_of_leds=number_of_leds)
red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

# same colors as normaln rgb, just 0 added at the end
colors_rgbw = [color+tuple([0]) for color in colors_rgb]
colors_rgbw.append((0, 0, 0, 255))

# uncomment colors_rgbw if you have RGBW strip
colors = colors_rgb
# colors = colors_rgbw

sd = components.sd_card()
lcd_display = components.lcd_display()
font = XglcdFont('TimesNR28x25.h', 28, 25)

ultrasonic_sensor = components.ultrasonic_sensor()

potentiometer = components.potentiometer()
pot_max = 65535
pot_min = 208
pot_diff = pot_max - pot_min

microphone = components.microphone()

led = Pin('LED', Pin.OUT)
baseline = 25000 # You may need to change this, but your mic should be reading around here as a baseline. 
variability = 0.1 # By being more selective about what we conside a spike, we can filter out noise. 10% is a good base level for a quiet room. 

servo = components.servo()
button = components.button(is_PULL_DOWN=True)

# Initialize Button
button = Pin(22, Pin.IN, Pin.PULL_DOWN)
print('Finished Initializing')

base_state = Base_State(lcd_display=lcd_display)
warm_up_state = Warm_Up(lcd_display=lcd_display)
workout_state = Workout(lcd_display=lcd_display)
# -------------------------------------------------------------------------
idle = True
warm_up = False
workout = False

while True:
    distance = ultrasonic_sensor.distance_cm()

    if idle:
        state = base_state
    elif warm_up:
        state = warm_up_state
    else:
        state = workout

    if distance > 100:
        state.idle('^_^')
