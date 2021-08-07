from lib.rest_client import RestClient

class ISS:
    def __init__(self):
        self.client = RestClient(
            '',
            { 'host': 'http://api.open-notify.org' }
        )
        # self.client.debug(True)

    def get_location(self):
        location = None

        resp = self.client.get("/iss-now.json")
        if resp.status_code == 200:
            data = resp.json()
            location = (
                float(data['iss_position']['latitude']),
                float(data['iss_position']['longitude'])
            )


        return location
