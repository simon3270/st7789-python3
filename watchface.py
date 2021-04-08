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
  * round  - 240x240 1.3" Round LCD (default)
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

font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

t_start = time.time()

# get numeral positions
nums_pos = []
onetick_ends = []
fivetick_ends = []
FULL_RADIUS = WIDTH/2
TICK_5_INNER = FULL_RADIUS - 7
TICK_5_WIDTH = 4
TICK_1_INNER = FULL_RADIUS - 5
TICK_1_WIDTH = 2
NUMRADIUS = FULL_RADIUS - 18
HOUR_RADIUS = FULL_RADIUS - 45
HOUR_WIDTH = 8
MINUTE_RADIUS = FULL_RADIUS - 35
MINUTE_WIDTH = 6
SECOND_RADIUS = FULL_RADIUS - 25
SECOND_WIDTH = 1

for ii in range(12):
    nums_pos.append((int(MID_X+NUMRADIUS*math.sin((ii+1)*2*math.pi/12.0)-10),
                     int(MID_Y-10-NUMRADIUS*math.cos((ii+1)*2*math.pi/12.0))))

for ii in range(60):
    onetick_ends.append((int(MID_X+TICK_1_INNER*math.sin(ii*2*math.pi/60.0)),
                         int(MID_Y+TICK_1_INNER*math.cos(ii*2*math.pi/60.0)),
                         int(MID_X+FULL_RADIUS*math.sin(ii*2*math.pi/60.0)),
                         int(MID_Y+FULL_RADIUS*math.cos(ii*2*math.pi/60.0))))
for ii in range(12):
    fivetick_ends.append((int(MID_X+TICK_5_INNER*math.sin(ii*2*math.pi/12.0)),
                          int(MID_Y+TICK_5_INNER*math.cos(ii*2*math.pi/12.0)),
                          int(MID_X+FULL_RADIUS*math.sin(ii*2*math.pi/12.0)),
                          int(MID_Y+FULL_RADIUS*math.cos(ii*2*math.pi/12.0))))


while True:
    # Clear out image
    draw.rectangle((0, 0, 240, 240), fill=(0, 0, 0, 0))
    # Draw the numbers round the edge
    for ii in range(12):
        draw.text(nums_pos[ii], "%d" % (ii+1), font=font, fill=(255, 255, 255))
        draw.line(fivetick_ends[ii], (192, 192, 192), width=TICK_5_WIDTH)
    for ii in range(60):
        if ii % 5 != 0:
            draw.line(onetick_ends[ii], (192, 192, 192), width=TICK_1_WIDTH)
    # Get the current time, and work out the hand direction
    t_now = time.localtime()
    h_dirn = (t_now.tm_hour+t_now.tm_min/60.0)*2*math.pi/12.0
    m_dirn = (t_now.tm_min+t_now.tm_sec/60.0)*2*math.pi/60.0
    s_dirn = (t_now.tm_sec)*2*math.pi/60.0
    # Draw the hands as lines of verying widths
    draw.line((MID_X, MID_Y,
               MID_X+HOUR_RADIUS*math.sin(h_dirn),
               MID_Y-HOUR_RADIUS*math.cos(h_dirn)),
              (0, 0, 255), width=HOUR_WIDTH)
    draw.line((MID_X, MID_Y,
               MID_X+MINUTE_RADIUS*math.sin(m_dirn),
               MID_Y-MINUTE_RADIUS*math.cos(m_dirn)),
              (0, 255, 0), width=MINUTE_WIDTH)
    draw.line((MID_X, MID_Y,
               MID_X+SECOND_RADIUS*math.sin(s_dirn),
               MID_Y-SECOND_RADIUS*math.cos(s_dirn)),
              (255, 0, 0), width=SECOND_WIDTH)
    draw.ellipse((MID_X-5, MID_Y-5, MID_X+5, MID_Y+5),
                 outline=(0, 255, 0), fill=(0, 0, 255))
    # Display the time digitally too
    time_str = "%2d:%02d:%02d" % \
        (t_now.tm_hour, t_now.tm_min, t_now.tm_sec)
    size_x, size_y = draw.textsize(time_str, font)
    draw.text((MID_X-size_x/2, MID_Y+30), time_str,
              font=font, fill=(128, 128, 128))
    # Refresh the display
    disp.display(img)

    # Pause a moment - don't wait for the whole second, otherwise
    # the display gets too jumpy (the above code takes time to run)
    time.sleep(0.1)
