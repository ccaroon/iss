from lib.rest_client import RestClient
from rgbxy import Converter, GamutC

class HueLight:
    BRIDGE_HOST  = None
    BRIDGE_TOKEN = None
    CONVERTER    = Converter(GamutC)
    REST_CLIENT  = None

    def __init__(self, id, data={}):
        if not self.REST_CLIENT:
            raise Exception("HueLights must first be initialized!")
        else:
            self.id   = id
            self.data = data
            self.initial_state = data.get('state', {'on': False}).copy()
            # fields that are not modifyable
            for fld in ('colormode', 'effect', 'alert', 'mode', 'reachable'):
                del self.initial_state[fld]

    @classmethod
    def init(cls, host, token):
        cls.BRIDGE_HOST  = host
        cls.BRIDGE_TOKEN = token

        cls.REST_CLIENT = RestClient(F'/api/{cls.BRIDGE_TOKEN}', {
            'host': cls.BRIDGE_HOST
        })

    @classmethod
    def get_by_name(cls, name):
        light = None

        resp = cls.REST_CLIENT.get('/lights')
        RestClient.error(resp)

        lights = resp.json()
        for id, data in lights.items():
            if data['name'] == name:
                light = HueLight(id, data)
                break

        return light

    def name(self):
        return self.data['name']

    def reload(self):
        pass

    def reset(self):
        """ Reset the light to it's inital state """
        resp = self.REST_CLIENT.put(F"/lights/{self.id}/state", self.initial_state)
        RestClient.error(resp)
        self.data['state'] = self.initial_state

    def color(self, rgb = None):
        """ Get/Set Color """
        if rgb:
            xy = self.CONVERTER.rgb_to_xy(rgb[0], rgb[1], rgb[2])
            resp = self.REST_CLIENT.put(F"/lights/{self.id}/state", {
                'xy': xy
            })

            RestClient.error(resp)
            self.data['state']['xy'] = xy
        else:
            xy = self.data['state']['xy']
            return (self.CONVERTER.xy_to_rgb(xy[0], xy[1]))

    def on(self, value=None):
        """ Get/Set Current ON state """
        if value:
            resp = self.REST_CLIENT.put(F"/lights/{self.id}/state", {
                'on': value
            })

            RestClient.error(resp)
            self.data['state']['on'] = value
        else:
            return self.data['state']['on']









#
