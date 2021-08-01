#!/usr/bin/env python
import os
import random
# TODO: update to use rest_client instead of requests directly
import requests
import sys
import time
import yaml

from lib.hue_bridge import HueBridge
from lib.gps_area import GPSArea
# ------------------------------------------------------------------------------
LOG_LEVEL=1
# ------------------------------------------------------------------------------
def log(msg, level=1):
    if level <= LOG_LEVEL:
        print(F"ISS - ({level}) {msg}")
# ------------------------------------------------------------------------------
def iss_overhead(light, places, simulate=False):
    being_controlled = False
    # For simulate
    all_places = list(places)
    all_places.append(None)

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
            # Check list of places
            curr_place = None
            if simulate:
                curr_place = random.choice(all_places)
            else:
                for place in places:
                    log(F"Checking '{place['name']}' [{place['color']}]", 3)
                    if place['area'].contains(iss_location):
                        curr_place = place

            # Report results
            if curr_place:
                if being_controlled == False:
                    being_controlled = True
                    light.reload()
                    light.brightness(75)

                light.color(curr_place['color'])
                log(F"The ISS is over {curr_place['name']} right now.")
            else:
                # if we control light, then reset to original state/color
                if being_controlled:
                    being_controlled = False
                    light.reset()

                log("The ISS is NOT overhead right now.")
                log(F"https://www.google.com/maps/search/{iss_location[0]},+{iss_location[1]}/@{iss_location[0]},{iss_location[1]},4z")
        else:
            log(F"Error: Unable to get ISS location: {err_msg}")

        time.sleep(10)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    log("--==> BEGIN <==--")

    config = None
    with open(F"{os.getenv('HOME')}/.config/iss-hue.yml", 'r') as cfile:
        config = yaml.safe_load(cfile)

    hue = HueBridge(config['host'], config['token'])
    light = hue.get_light('Couch Light')

    durham = GPSArea.from_file("./data/durham.coords", reverse=True)
    nc     = GPSArea.from_file("./data/nc.coords", reverse=True)
    usa    = GPSArea.from_file("./data/usa.coords", reverse=True)

    try:
        # List of places should be largest to smallest area size-wise in the list
        iss_overhead(light, (
            {'name': "The USA",        'color': (128,128,128), 'area': usa},
            {'name': "North Carolina", 'color': (0,0,255),     'area': nc},
            {'name': "Durham",         'color': (0,255,0),     'area': durham}
        ), simulate=False)
    except Exception as e:
        log(F"Error: {e}")
        light.color((64,0,0))
        time.sleep(30)
        light.reset()
        log("--==> END <==--")
        sys.exit(1)






#
