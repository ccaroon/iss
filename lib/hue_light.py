import time
from lib.rest_client import RestClient
from rgbxy import Converter, GamutC

class HueLight:
    CONVERTER = Converter(GamutC)

    def __init__(self, bridge, id, data={}):
        self.bridge = bridge
        self.__client = bridge.client

        self.id   = id
        self.data = data
        self.__set_initial_state()

    def __set_initial_state(self):
        self.initial_state = self.data.get('state', {'on': False}).copy()
        # fields that are not modifyable
        for fld in ('colormode', 'effect', 'alert', 'mode', 'reachable'):
            if fld in self.initial_state:
                del self.initial_state[fld]

    def name(self):
        return self.data['name']

    def reload(self):
        """ Reload the lights state """
        resp = self.__client.get(F"/lights/{self.id}")

        self.data = resp.json()
        self.__set_initial_state()

    def reset(self):
        """ Reset the light to it's inital state """
        resp = self.__client.put(F"/lights/{self.id}/state", self.initial_state)
        self.data['state'] = self.initial_state

    def color(self, rgb = None):
        """ Get/Set Color """

        if rgb:
            xy = self.CONVERTER.rgb_to_xy(rgb[0], rgb[1], rgb[2])
            resp = self.__client.put(F"/lights/{self.id}/state", {
                'xy': xy,
                'on': True
            })

            self.data['state']['xy'] = xy
        else:
            xy = self.data['state']['xy']
            return (self.CONVERTER.xy_to_rgb(xy[0], xy[1]))

    # percent: 0 to 100
    def brightness(self, percent:int=None):
        """ Get/Set Brightness """
        if percent is not None:
            # translate percent to value between 0 & 254
            bri_value = int(254 * (percent/100))
            resp = self.__client.put(F"/lights/{self.id}/state", {
                'bri': bri_value,
                'on': True
            })

            self.data['state']['bri'] = bri_value
        else:
            return self.data['state']['bri']

    def on(self, value=None):
        """ Get/Set Current ON state """
        if value in (True, False):
            resp = self.__client.put(F"/lights/{self.id}/state", {
                'on': value
            })

            self.data['state']['on'] = value
        else:
            return self.data['state']['on']

    def blink(self, color, count=3):
        self.on(True)
        self.color(color)

        for i in range(0, count):
            self.on(False)
            time.sleep(0.5)
            self.on(True)
            time.sleep(0.5)

        self.reset()
