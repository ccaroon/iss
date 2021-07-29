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
        self.initial_state = data.get('state', {'on': False}).copy()
        # fields that are not modifyable
        for fld in ('colormode', 'effect', 'alert', 'mode', 'reachable'):
            del self.initial_state[fld]

    def name(self):
        return self.data['name']

    # TODO: reload the lights state
    def reload(self):
        pass

    def reset(self):
        """ Reset the light to it's inital state """
        resp = self.__client.put(F"/lights/{self.id}/state", self.initial_state)
        RestClient.error(resp)
        self.data['state'] = self.initial_state

    def color(self, rgb = None):
        """ Get/Set Color """

        if rgb:
            if not self.on():
                self.on(True)

            xy = self.CONVERTER.rgb_to_xy(rgb[0], rgb[1], rgb[2])
            resp = self.__client.put(F"/lights/{self.id}/state", {
                'xy': xy
            })

            RestClient.error(resp)
            self.data['state']['xy'] = xy
        else:
            xy = self.data['state']['xy']
            return (self.CONVERTER.xy_to_rgb(xy[0], xy[1]))

    def on(self, value=None):
        """ Get/Set Current ON state """
        if value in (True, False):
            resp = self.__client.put(F"/lights/{self.id}/state", {
                'on': value
            })

            RestClient.error(resp)
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








#