import time
import board
import displayio
import terminalio
import adafruit_lis3mdl
import math

# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107

displayio.release_displays()
# oled_reset = board.D9

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C) # connect to the display
sensor = adafruit_lis3mdl.LIS3MDL(i2c) # connect to the magnetometer

########################
#Set up the display

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2
REFRESH_TIME = 0.5

display = adafruit_displayio_sh1107.SH1107(
    display_bus, width=WIDTH, height=HEIGHT, rotation=0
)

# Make the display context
splash = displayio.Group()
display.show(splash)


# Draw a smaller inner rectangle in black
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)




###########
# continuously measure and display the magnetic field

SAMPLE_NUM = 10

while True:
    #measure the field values and average over SAMPLE_NUM    
    mag_x, mag_y, mag_z = sensor.magnetic
    for i in range(SAMPLE_NUM-1):
        mag_x2, mag_y2, mag_z2 = sensor.magnetic
        mag_x += mag_x2
        mag_y += mag_y2
        mag_z += mag_z2
    mag_x, mag_y, mag_z = mag_x/SAMPLE_NUM, mag_y/SAMPLE_NUM, mag_z/SAMPLE_NUM
        
    #display Bx
    yb = 8
    text1 = "Bx = " + str(mag_x) + " uT"
    text_area1 = label.Label(terminalio.FONT, text=text1, scale=1, x=8, y=yb)    
    splash.append(text_area1)
    #display By
    text2 = "By = " + str(mag_y) + " uT"
    text_area2 = label.Label(terminalio.FONT, text=text2, scale=1, x=8, y=yb+15)    
    splash.append(text_area2)
    #display Bz
    text3 = "Bz = " + str(mag_z) + " uT"
    text_area3 = label.Label(terminalio.FONT, text=text3, scale=1, x=8, y=yb+30)    
    splash.append(text_area3)
    #display the magnitude of B
    text4 = "|B| = " + str(math.sqrt(mag_x**2+mag_y**2+mag_z**2))+ " uT"
    text_area4 = label.Label(terminalio.FONT, text=text4, scale=1, x=8, y=yb+45)    
    splash.append(text_area4)
    #display "by Andrei"
    
    y1 = 1
    splash.append(label.Label(terminalio.FONT, text="c", scale=1, x=112, y=y1))
    splash.append(label.Label(terminalio.FONT, text="o", scale=1, x=112, y=y1+10))
    splash.append(label.Label(terminalio.FONT, text="d", scale=1, x=112, y=y1+20))
    splash.append(label.Label(terminalio.FONT, text="e", scale=1, x=112, y=y1+30))
    
    y2 = y1 + 45
    splash.append(label.Label(terminalio.FONT, text="b", scale=1, x=112, y=y2))
    splash.append(label.Label(terminalio.FONT, text="y", scale=1, x=112, y=y2+10))
    
    splash.append(label.Label(terminalio.FONT, text="A", scale=1, x=123, y=5))
    splash.append(label.Label(terminalio.FONT, text="n", scale=1, x=123, y=15))
    splash.append(label.Label(terminalio.FONT, text="d", scale=1, x=123, y=25))
    splash.append(label.Label(terminalio.FONT, text="r", scale=1, x=123, y=35))
    splash.append(label.Label(terminalio.FONT, text="e", scale=1, x=123, y=43))
    splash.append(label.Label(terminalio.FONT, text="i", scale=1, x=123, y=55))
    #refresh the display
    display.show(splash)
    time.sleep(REFRESH_TIME)
    splash = displayio.Group()
