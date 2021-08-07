from lib.rest_client import RestClient
from lib.hue_light import HueLight

class HueBridge:
    def __init__(self, host, token):
        self.client = RestClient(
            F'/api/{token}',
            { 'host': host },
            self.error
        )
        # self.client.debug(True)

    def get_light(self, name):
        light = None

        resp = self.client.get('/lights')

        lights = resp.json()
        for id, data in lights.items():
            if data['name'] == name:
                light = HueLight(self, id, data)
                break

        return light

    def error(self, response):
        """Parse out the error message from the given response if any"""

        data = response.json()
        for result in data:
            error_msg = None
            if 'error' in result:
                error = result['error']
                error_msg = F"Status Code: [{response.status_code}] | Reason: [{response.reason}]"
                error_msg += F" | Description: [{error.get('description', '?????')}]"

                raise Exception(error_msg)
