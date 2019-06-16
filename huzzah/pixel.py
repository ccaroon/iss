from neopixel import NeoPixel
from machine import Pin

class Pixel:
    """Class representing a single NeoPixel"""

    def __init__(self, pin_num):
        pin = Pin(pin_num, Pin.OUT)
        self.__pixels = NeoPixel(pin, 1)

    def off(self):
        self.__pixels[0] = (0,0,0)
        self.__pixels.write()

    def white(self):
        self.__pixels[0] = (128,128,128)
        self.__pixels.write()

    def red(self):
        self.__pixels[0] = (128,0,0)
        self.__pixels.write()

    def green(self):
        self.__pixels[0] = (0,128,0)
        self.__pixels.write()

    def blue(self):
        self.__pixels[0] = (0,0,128)
        self.__pixels.write()

    def color(self, color):
        self.__pixels[0] = color
        self.__pixels.write()
