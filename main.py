from machine import I2C, Pin, SPI, ADC, PWM
from imu import MPU6050
from neopixel import Neopixel
from ili9341 import Display, color565
from hcsr04 import HCSR04
from xglcd_font import XglcdFont
from wavePlayer import wavePlayer
from servo import Servo
import time, os, sdcard, tm1637

from states import Base_State, Warm_Up, Workout
from component_classes import Components
from exercise import Exercise

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
# distance = ultrasonic_sensor.distance_cm()

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

print('Finished Initializing')
# -------------------------------------------------------

def reversed_string(text):
    result = ""
    for char in text:
        result = char + result
        
    return result

def draw_text2(x, y, text):
    lcd_display.draw_text(0 + y, 320 - x, reversed_string(text), font, color565(0,0,0), color565(255,255,255), True, True, 1)

def menu(input_options):
    options = [i for i in input_options]
    cur_option = -1
    options.insert(0, 'Exit')
    num_options = len(options)
    
    print(options)
    
    while True:
        time.sleep(0.1)
        option = round(potentiometer.read_u16() / pot_max * (num_options - 1))
        
        # print(potentiometer.read_u16())
        if option != cur_option:
            lcd_display.clear()
            lcd_display.fill_hrect(0, 0, 240, 320, color565(255,255,255))
            for i in range(num_options - option):
                try:
                    draw_text2(5, 5 + (i * 30),  f' {options[option + i].name}')
                except:
                    draw_text2(5, 5 + (i * 30),  f' {options[option + i]}')
            draw_text2(5, 5, '>')
            
        if button.value():
            print(option)
            return options[option]
        
        cur_option = option


# -------------------------------------------------

pushups = Exercise('Pushups')
dips = Exercise('Dips')
knee_pushups = Exercise('Knee Pushups')
bench_dips = Exercise('Bench Dips')
decline_pushups = Exercise('Decline Pushups')
weighted_dips = Exercise('Weighted Dips')

# -------------------------------------------------

menu_options = {
    "Calisthenics": {
        "Chest/Triceps": [pushups, dips, knee_pushups, bench_dips, decline_pushups, weighted_dips]
    }
}

timer = 0
tenths = 0

selection = 0
program = 0
program_complete = True
exercise_goal = 2
exercises_done = 2
exercise_complete = True

ring_light.fill(red)
ring_light.show()

base_state = Base_State(lcd_display=lcd_display)
warm_up_state = Warm_Up(lcd_display=lcd_display)
workout_state = Workout(lcd_display=lcd_display)
# -------------------------------------------------------------------------
idle = True
warm_up = False
workout = False

while (selection != 'Exit'):
#     ring_light.rotate_right(1)
#     ring_light.show()
#     
#     try:
#         distance = ultrasonic_sensor.distance_cm()
#         print('Distance:', distance, 'cm')
#     except OSError as ex:
#         print('ERROR getting distance:', ex)
    distance = ultrasonic_sensor.distance_cm()

    if idle == True and warm_up_state == False and workout_state == False:
        state = base_state
    elif idle == False and warm_up_state == True and workout_state == False:
        state = warm_up_state
    elif idle == False and warm_up_state == False and workout_state == True:
        state = workout_state

    if distance > 100:
        state.idle('^_^')
    

    # If we detect a spike in the waveform greater than a 10% deviation from our baseline, someone is probably talking.
    if microphone.read_u16() > (baseline + baseline*variability) or microphone.read_u16() < (baseline - baseline*variability):
        led.on() # Turn the light on if we're detecting a spike
    else:
        led.off() # Otherwise, keep the light off
    
#     x1 = potentiometer.read_u16()
#     x = (x1/65535) * 180
#     servo.move(x)
    
    selection = menu(menu_options)
    program = menu(menu_options[selection])
    exercise_name = menu(menu_options[selection][program])
    exercise_type = menu(['Timed', 'Reps'])
    if (exercise_type == 'Timed'):
        exercise_time = menu([30, 60, 90, 120])
        exercise_name.timed_exercise(exercise_time)
    else:
        exercise_name.rep_exercise()
