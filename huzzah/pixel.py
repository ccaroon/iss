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

    def white(self, intensity=128):
        self.__pixels[0] = (intensity,intensity,intensity)
        self.__pixels.write()

    def red(self, intensity=128):
        self.__pixels[0] = (intensity,0,0)
        self.__pixels.write()

    def green(self, intensity=128):
        self.__pixels[0] = (0,intensity,0)
        self.__pixels.write()

    def blue(self, intensity=128):
        self.__pixels[0] = (0,0,intensity)
        self.__pixels.write()

    # color: Tuple (R,G,B)
    def color(self, color):
        self.__pixels[0] = color
        self.__pixels.write()

    @classmethod
    def test(cls, pin_num = 15, delay = 1):
        pixel = Pixel(pin_num)

        while True:
            pixel.white()
            print("White")
            utime.sleep(delay)

            pixel.red()
            print("Red")
            utime.sleep(delay)

            pixel.blue()
            print("Blue")
            utime.sleep(delay)

            pixel.green()
            print("Green")
            utime.sleep(delay)
