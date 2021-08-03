#!/usr/bin/env python
import os
import random
# TODO: update to use rest_client instead of requests directly
import requests
import sys
import time
import yaml

from lib.blynk_handler import BlynkHandler
from lib.hue_handler import HueHandler
from lib.gps_area import GPSArea
# ------------------------------------------------------------------------------
LOG_LEVEL=1
# ------------------------------------------------------------------------------
def log(msg, level=1):
    if level <= LOG_LEVEL:
        print(F"ISS - ({level}) {msg}")
# ------------------------------------------------------------------------------
def track_iss(places, handlers):
    being_controlled = False

    last_place = None
    while (True):
        log("-----------------------------------------------------------------")

        # Get ISS position
        iss_location = None
        err_msg = None
        try:
            resp = requests.get("http://api.open-notify.org/iss-now.json")

            if resp.status_code == 200:
                data = resp.json()
                iss_location = (
                    float(data['iss_position']['latitude']),
                    float(data['iss_position']['longitude'])
                )
            else:
                err_msg = F"{resp.status_code} - {resp.text}"
        except Exception as e:
            err_msg = F"{e}"

        if iss_location is not None:
            for handler in handlers:
                handler.location(iss_location)

            # Check list of places
            known_place = None
            for place in places:
                log(F"Checking '{place['name']}' [{place['color']}]", 3)
                if place['area'].contains(iss_location):
                    known_place = place

            for handler in handlers:
                handler.known_place(known_place)

            if known_place:
                log(F"The ISS is over {known_place['name']} right now.")
            else:
                log("The ISS is NOT overhead right now.")
                log(F"https://www.google.com/maps/search/{iss_location[0]},+{iss_location[1]}/@{iss_location[0]},{iss_location[1]},4z")
        else:
            log(F"Error: Unable to get ISS location: {err_msg}")

        time.sleep(10)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    log("--==> BEGIN <==--")
    handlers = []

    config = None
    with open(F"{os.getenv('HOME')}/.config/iss-hue.yml", 'r') as cfile:
        config = yaml.safe_load(cfile)

    blynk_cfg = config.get('blynk', {})
    blynk_map = BlynkHandler('BlynkMap', blynk_cfg)
    handlers.append(blynk_map)

    # hue_cfg = config.get('hue', {})
    # hue_handler = HueHandler('CD1', hue_cfg)
    # handlers.append(hue_handler)

    durham = GPSArea.from_file("./data/durham.coords", reverse=True)
    nc     = GPSArea.from_file("./data/nc.coords", reverse=True)
    usa    = GPSArea.from_file("./data/usa.coords", reverse=True)

    try:
        # List of places should be largest to smallest area size-wise in the list
        track_iss(
            (
                {'name': "The USA",        'color': (128,128,128), 'area': usa},
                {'name': "North Carolina", 'color': (0,0,255),     'area': nc},
                {'name': "Durham",         'color': (0,255,0),     'area': durham}
            ),
            handlers
        )
    except Exception as e:
        for handler in handlers:
            handler.error(F"ISS Error: {e}")

        log(F"Error: {e}")
        log("--==> END <==--")
        sys.exit(1)






#
