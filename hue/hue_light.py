import requests

from rgbxy import Converter, GamutC

class HueLight:
    BRIDGE_HOST  = None
    BRIDGE_TOKEN = None
    END_POINT    = None
    CONVERTER    = Converter(GamutC)

    def __init__(self, id, data={}):
        if not self.END_POINT:
            raise Exception("HueLights must first be initialized!")
        else:
            self.id   = id
            self.data = data
            self.initial_state = data.get('state', {'on': False})

    @classmethod
    def init(cls, host, token):
        cls.BRIDGE_HOST  = host
        cls.BRIDGE_TOKEN = token
        cls.END_POINT = F"http://{cls.BRIDGE_HOST}/api/{cls.BRIDGE_TOKEN}"

    @classmethod
    def get_by_name(cls, name):
        light = None

        resp = requests.get(F"{cls.END_POINT}/lights")
        if resp.ok:
            lights = resp.json()
        else:
            raise Exception(resp.text)

        for id, data in lights.items():
            if data['name'] == name:
                light = HueLight(id, data)
                break

        return light

    def name(self):
        return self.data['name']

    def reset(self):
        """ Reset the light to it's inital state """
        # TODO: use self.initial_state
        pass

    def color(self, rgb = None):
        """ Get/Set Color """
        if rgb:
            xy = CONVERTER.rgb_to_xy(rgb[0], rgb[1], rgb[2])
            resp = requests.put(F"{self.END_POINT}/lights/{self.id}/state", json={
                'xy': xy
            })
            if resp.ok:
                data = resp.json()[0]
                if data.get('error', None):
                    # print(data['error'])
                    raise Exception(data['error']['description'])
                else:
                    pass
            else:
                raise Exception(resp.text)
        else:
            xy = self.data['state']['xy']
            return (CONVERTER.xy_to_rgb(xy[0], xy[1]))

    def on(self, value=None):
        """ Get/Set Current ON state """
        if value:
            pass
        else:
            return self.data['state']['on']
