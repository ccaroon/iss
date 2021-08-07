from lib.rest_client import RestClient
from lib.hue_light import HueLight

class HueBridge:
    def __init__(self, host, token):
        self.__host = host
        self.__token = token
        self.client = RestClient.new_instance(F'/api/{token}', {
            'host': host
        })
        # self.client.debug(True)

    def get_light(self, name):
        light = None

        resp = self.client.get('/lights')
        RestClient.error(resp)

        lights = resp.json()
        for id, data in lights.items():
            if data['name'] == name:
                light = HueLight(self, id, data)
                break

        return light
