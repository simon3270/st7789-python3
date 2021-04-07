# st7789-python3
Example ST7789 display code in Python3

## Watch face - watchface.py

This is an analogue watch, particularly aimed at the [Pimoroni 1.3" SPI Colour Round LCD (240x240) Breakout](https://shop.pimoroni.com/products/1-3-spi-colour-round-lcd-240x240-breakout), though it should work on many SPI st7789 displays (or, with some tweaks, I2C ones).

The code is executable. Usage:

    ./watchface.py [round|square]

The only parameter is whether the display is round (default) or square. It was developed for the Pimoroni 240 by 240 round display, but has also been tested on the [square one](https://shop.pimoroni.com/products/1-3-spi-colour-lcd-240x240-breakout).
