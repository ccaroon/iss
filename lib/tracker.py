import time

from lib.iss import ISS

class Tracker:
    def __init__(self, name, places, handlers):
        self.name = name
        self.__iss = ISS()
        self.__places = places
        self.__handlers = handlers

    def run(self):
        while True:
            try:
                self.update()
                time.sleep(10)
            except Exception as e:
                for handler in self.__handlers:
                    handler.error(F"{self.name} Error: {e}")
                raise e

    def update(self):
        err_msg = None
        iss_location = None

        try:
            iss_location = self.__iss.get_location()
        except Exception as e:
            err_msg = str(e)

        if iss_location is not None:
            for handler in self.__handlers:
                handler.location(iss_location)

            # Check list of places
            known_place = None
            for place in self.__places:
                # self.__log(F"Checking '{place['name']}' [{place['color']}]")
                if place['area'].contains(iss_location):
                    known_place = place

            for handler in self.__handlers:
                handler.known_place(known_place)

            if known_place:
                self.__log(F"The ISS is over {known_place['name']} right now.")
            else:
                self.__log("The ISS is NOT overhead right now.")
                self.__log(F"https://www.google.com/maps/search/{iss_location[0]},+{iss_location[1]}/@{iss_location[0]},{iss_location[1]},4z")
        else:
            self.__log(F"Error: Unable to get ISS location: {err_msg}")

    def __log(self, msg):
        print(F"{self.name} - {msg}")
