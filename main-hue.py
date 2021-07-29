#!/usr/bin/env python
import time
import random
# TODO: update to use rest_client
import requests
import yaml

from lib.hue_bridge import HueBridge
from lib.gps_area import GPSArea
# ------------------------------------------------------------------------------
PRINT=True
LOG_FILE = "iss.log"
# ------------------------------------------------------------------------------
def log(msg):
    if PRINT:
        print(msg)

    with open(LOG_FILE, "a") as file:
        file.write("%d - %s\n" % (time.time(), msg))
# ------------------------------------------------------------------------------
def iss_overhead(hue_light, places, simulate=False):
    being_controlled = False
    # For simulate
    all_places = list(places)
    all_places.append(None)

    while (True):
        log("-------------------------")
        # Get ISS position
        resp = requests.get("http://api.open-notify.org/iss-now.json")
        if resp.status_code == 200:
            data = resp.json()
            iss = (float(data['iss_position']['latitude']), float(data['iss_position']['longitude']))
            # Check list of places
            curr_place = None
            if simulate:
                curr_place = random.choice(all_places)
            else:
                for place in places:
                    log("Checking '%s' [%s]" % (place['name'], place['color']))
                    if place['area'].contains(iss):
                        curr_place = place

            # Report results
            if curr_place:
                being_controlled = True
                light.color(curr_place['color'])
                log("The ISS is over %s right now." % (curr_place['name']))
            else:
                # if we control light, then reset to original state/color
                if being_controlled:
                    light.reset()
                    being_controlled = False
                log("The ISS is NOT overhead right now.")
                log("https://www.google.com/maps/search/%f,+%f/@%f,%f,4z" % (iss[0], iss[1], iss[0] ,iss[1]))
        else:
            light.color((16,0,0))
            log("Error Getting ISS Location: %s" % (resp.status_code))

        log("-------------------------")
        time.sleep(10)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    log("--==> BEGIN <==--")

    config = None
    with open('.secrets.yml', 'r') as secrets:
        config = yaml.safe_load(secrets)

    hue = HueBridge(config['host'], config['token'])
    light = hue.get_light('Couch Light')

    # light.blink((0,255,255), count=2)

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
        log("Error: %s" % (e))
        light.color((255,0,0))



#