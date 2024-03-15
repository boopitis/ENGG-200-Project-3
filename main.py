from utility import Utility
from component_classes import Components

from machine import Pin
from xglcd_font import XglcdFont
import time

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
    button_pin = 22,
)

# Initialize Utility
TNR = XglcdFont('TimesNR28x25.h', 28, 25)
ut = Utility(TNR)

# Initialize Components ---------------------------------
player = components.speaker()
segment_display = components.segment_display()

number_of_leds = 8
ring_light = components.ring_light(default_brightness=10, number_of_leds=number_of_leds)

sd = components.sd_card()
lcd_display = components.lcd_display()

ultrasonic_sensor = components.ultrasonic_sensor()
distance = ultrasonic_sensor.distance_cm()

potentiometer = components.potentiometer()
pot_max = 65535
pot_min = 208
pot_diff = pot_max - pot_min

microphone = components.microphone()

led = Pin('LED', Pin.OUT)
baseline = 29000 # You may need to change this, but your mic should be reading around here as a baseline. 
variability = 0.1 # By being more selective about what we conside a spike, we can filter out noise. 10% is a good base level for a quiet room. 

servo = components.servo()
button = components.button(is_PULL_DOWN=True)

# Initialize Button
button = Pin(22, Pin.IN, Pin.PULL_DOWN)
print('Finished Initializing')
# -------------------------------------------------------

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

step = round(number_of_leds / len(colors))
current_pixel = 0

for color1, color2 in zip(colors, colors[1:]):
    ring_light.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
    current_pixel += step

ring_light.set_pixel_line_gradient(current_pixel, number_of_leds - 1, violet, red)

segment_display.show('0420', True)

while True:
    ring_light.rotate_right(1)
    ring_light.show()
    
    try:
        distance = ultrasonic_sensor.distance_cm()
        print('Distance:', distance, 'cm')
    except OSError as ex:
        print('ERROR getting distance:', ex)
        
    # If we detect a spike in the waveform greater than a 10% deviation from our baseline, someone is probably talking.
    if microphone.read_u16() > (baseline + baseline*variability) or microphone.read_u16() < (baseline - baseline*variability):
        led.on() # Turn the light on if we're detecting a spike
    else:
        led.off() # Otherwise, keep the light off
    
    x1 = potentiometer.read_u16()
    x = (x1/65535) * 180
    servo.move(x)
    
    time.sleep(0.1)