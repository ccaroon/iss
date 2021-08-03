import blynklib

from lib.location_handler import LocationHandler

class BlynkHandler(LocationHandler):
    MAP_VPIN = 1

    def __init__(self, name, config):
        super().__init__(name, config)

        self.__blynk = blynklib.Blynk(config['token'])
        self.__blynk.run()

    def location(self, long_lat):
        self.__blynk.run()
        self.__blynk.virtual_write(
            self.MAP_VPIN,
            0,
            long_lat[0],
            long_lat[1],
            "ISS"
        )

    # Blynk does not care if the ISS is over a known place
    def known_place(self, place):
        pass

    def error(self, err_msg):
        self.__blynk.notify(err_msg)
