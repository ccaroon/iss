import time

from lib.location_handler import LocationHandler
from lib.hue_bridge import HueBridge

class HueHandler(LocationHandler):
    def __init__(self, name, config):
        super.__init__(name, config)

        bridge = HueBridge(config['host'], config['token'])
        self.__light = bridge.get_light(name)

    # Hue does not care about the location, only about if the ISS is over a
    # know place
    def location(self, long_lat):
        pass

    def known_place(self, place):
        pass
        # if place is not None:
        #     if being_controlled == False:
        #         being_controlled = True
        #         light.reload()
        #         light.brightness(75)

        #     if known_place != last_place:
        #         last_place = known_place
        #         blynk.notify(F"The ISS is over {known_place['name']} right now.")

        #     light.color(known_place['color'])
        # else:
        #     # if we control light, then reset to original state/color
        #     if being_controlled:
        #         being_controlled = False
        #         light.reset()
        #         last_place = None

    def error(self, err_msg):
        self.__light.color((64,0,0))
        time.sleep(30)
        self.__light.reset()
