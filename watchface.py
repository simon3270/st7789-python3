#!/usr/bin/env python3

""" Display a Watch on an ST7789 display - preferably round!
"""

import sys
import math
import time
import colorsys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7789

print("""
watchface.py - Display a watch face, with second hand.

If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the front slot.

Usage: {} <display_type>

Where <display_type> is one of:

  * square - 240x240 1.3" Square LCD
  * round  - 240x240 1.3" Round LCD (applies an offset)
""".format(sys.argv[0]))

try:
    display_type = sys.argv[1]
except IndexError:
    display_type = "round"


# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000,
    offset_left=40 if display_type == "round" else 0
)

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

MID_X = WIDTH/2
MID_Y = HEIGHT/2

img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

t_start = time.time()

# get numeral positions
nums = []
NUMRADIUS = WIDTH/2 - 10
for ii in range(12):
    nums.append((int(MID_X+NUMRADIUS*math.sin((ii+1)*2*math.pi/12.0)-10),
                 int(MID_Y-10-NUMRADIUS*math.cos((ii+1)*2*math.pi/12.0))))

HOUR_RADIUS = WIDTH/2 - 45
HOUR_WIDTH = 8
MINUTE_RADIUS = WIDTH/2 - 35
MINUTE_WIDTH = 6
SECOND_RADIUS = WIDTH/2 - 25
SECOND_WIDTH = 1


while True:
    #x = (time.time() - t_start) * 100
    #x %= (size_x + disp.width)
    draw.rectangle((0, 0, 240, 240), fill=(0, 0, 0, 0))
    for ii in range(12):
        draw.text(nums[ii], "%d" % (ii+1), font=font, fill=(255, 255, 255))
    t_now = time.localtime()
    h_dirn = (t_now.tm_hour+t_now.tm_min/60.0)*2*math.pi/12.0
    m_dirn = (t_now.tm_min/60.0)*2*math.pi
    s_dirn = (t_now.tm_sec/60.0)*2*math.pi
    draw.line((MID_X, MID_Y, 
               MID_X+HOUR_RADIUS*math.sin(h_dirn),
               MID_Y-HOUR_RADIUS*math.cos(h_dirn)),
              (0,0,255), width=HOUR_WIDTH)
    draw.line((MID_X, MID_Y, 
               MID_X+MINUTE_RADIUS*math.sin(m_dirn),
               MID_Y-MINUTE_RADIUS*math.cos(m_dirn)),
              (0,255,0), width=MINUTE_WIDTH)
    draw.line((MID_X, MID_Y, 
               MID_X+SECOND_RADIUS*math.sin(s_dirn),
               MID_Y-SECOND_RADIUS*math.cos(s_dirn)),
              (255,0,0), width=SECOND_WIDTH)
    draw.ellipse((MID_X-5, MID_Y-5, MID_X+5, MID_Y+5),
            outline=(0, 255, 0), fill=(0, 0, 255))
    time_str = "%2d:%02d:%02d" % \
            (t_now.tm_hour, t_now.tm_min, t_now.tm_sec)
    size_x, size_y = draw.textsize(time_str, font)
    draw.text((MID_X-size_x/2, MID_Y+30), time_str,
            font=font, fill=(128, 128, 128))
    #draw.rectangle((MID_X-HOUR_WIDTH*math.cos(h_dirn-math.pi/2),
    #                MID_Y+HOUR_WIDTH*math.sin(h_dirn-math.pi/2),
    #                MID_X+HOUR_RADIUS*math.sin(h_dirn)-HOUR_WIDTH*math.cos(h_dirn+math.pi/2),
    #                MID_Y+HOUR_RADIUS*math.cos(h_dirn)+HOUR_WIDTH*math.sin(h_dirn+math.pi/2)),
    #               (0, 255, 0))
    #draw.text((int(text_x - x), text_y), MESSAGE, font=font, fill=(255, 255, 255))
    disp.display(img)
