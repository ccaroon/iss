import time

from lib.location_handler import LocationHandler
from phuey.hue_bridge import HueBridge

class HueHandler(LocationHandler):
    def __init__(self, name, config):
        super().__init__(name, config)

        bridge = HueBridge(config['host'], config['token'])
        self.__light = bridge.get_light(name)
        self.__active = False
        self.__last_place = None

        self.__light.blink((0,255,0), 1)

    # Hue does not care about the location, only about if the ISS is over a
    # know place
    def location(self, long_lat):
        pass

    def known_place(self, place):
        if place is not None:
            if self.__active == False:
                self.__active = True
                self.__light.reload()
                self.__light.brightness(75)

            if place != self.__last_place:
                self.__last_place = place

            self.__light.color(place['color'])
        else:
            # if we control self.__light, then reset to original state/color
            if self.__active:
                self.__active = False
                self.__light.reset()
                self.__last_place = None

    def error(self, err_msg):
        self.log(err_msg)
        self.__light.color((64,0,0))
        time.sleep(30)
        self.__light.reset()
