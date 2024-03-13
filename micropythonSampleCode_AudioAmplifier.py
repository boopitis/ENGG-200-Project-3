'''
    (c) 2021  Daniel Perron
    MIT License

    example of audio output using PWM and DMA
    right now it  works only with wave file at
    8000 sample rate , stereo or mono, and 16 bits audio

    GPIO  2 & 3  pin 4 and 5 are the output
    You need to use headphones with a 1K resistor in series on
    left and right speaker

    The myPWM subclass sets the maximum count to 255 at a frequency around  122.5KHz.

    The myDMA class allows to use direct memory access to transfer each frame at the current sample rate


    You need to install the wave.py and chunk.py  from
         https://github.com/joeky888/awesome-micropython-lib/tree/master/Audio
         
    SDCard.py  is available in  https://github.com/micropython/micropython/tree/master/drivers/sdcard
      please be sure to rename it SDCard.py into the pico lib folder
    

    ***  be sure to increase the SPI clock speed > 5MHz
    ***  once SDCard is initialize set the spi to an higher clock


    How it works,

       1 - We set the PWM  to a range of 255, 1023 for 10 bits, at 122Khz
       2 - We read the wave file using the class wave which will set the sample rate and read the audio data by chunk
       3 - Mono files are converted to stereo by duplicating the original audio samples
       4 - Each chunk are converted to  16 bit signed to unsigned char with the middle at 128
       5 - Wait for the DMA to be completed.  On first it will be anyway.
       6 - The converted chunk is then passed to the DMA to be transfered at the sample rate using one of built-in timer
       7 - Go on step 2 until is done.

    P.S. use rshell to transfer wave files to the Pico file system

    April 20
    Version 0.1
    ---  Add DMA chainning. This removes the glitch betweem DMA transfer
    ---  assembly function convert2PWM replace  the struct pack and compack
        since it is not necessary to convert the binary string it is way faster.
    Version 0.2
    ---  Add mono audio file handling

    For Headphones

    
             2K
    PIO2   -/\/\/-----+-----    headphone left
                      |
                     === 0.1uF
                      |
    PIO4   -----------+-----    headphone ground
                      |
                     === 0.1uF
              2k      |
    PIO3   -/\/\/-----+-----    headphone right



    For amplifier don't use PIO4 and the capacitor should be 2200pF and connected to GND. 

'''

import os
import sdcard
from wavePlayer import wavePlayer
from machine import Pin, SPI

player = wavePlayer(Pin(10), Pin(11))

# Initialize SD card
spi=SPI(0,baudrate=40000000,sck=Pin(2),mosi=Pin(3),miso=Pin(4))
sd=sdcard.SDCard(spi,Pin(5))
print('i')
vfs=os.VfsFat(sd)
os.mount(sd,'/sd')
print(os.listdir('/sd'))

# waveFolder= ""
# wavelist = []
# 
# for i in os.listdir('/sd'):
#     if i.find(".wav")>=0:
#         wavelist.append(waveFolder+"/"+i)
#     elif i.find(".WAV")>=0:
#         wavelist.append(waveFolder+"/"+i)
#         
# if not wavelist :
#     print("Warning NO '.wav' files")
# else:
#     print("Will play these '.wav' files","/n",wavelist)
#     try:
#         while True:
#             for i in wavelist:
#                 print(i)
#                 player.play(i)
#     except KeyboardInterrupt:
#         player.stop()

print(os.listdir('/sd')[2])
# player.play(os.listdir('/sd')[2])

print("wavePlayer terminated")


