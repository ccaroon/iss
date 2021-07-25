#!/usr/bin/env python
import time
import requests
import yaml

from hue_light import HueLight
from .. lib/gps_area import GPSArea

LOG_FILE = "iss.log"
def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as file:
        file.write("%d - %s\n" % (time.time(), msg))

# ------------------------------------------------------------------------------
def iss_overhead(hue_light, places):
    being_controlled = False

    while (True):
        # Get ISS position
        resp = requests.get("http://api.open-notify.org/iss-now.json")
        if resp.status_code == 200:
            data = resp.json()
            iss = (float(data['iss_position']['latitude']), float(data['iss_position']['longitude']))
            # Check list of places
            curr_place = None
            for place in places:
                # print("Checking '%s' [%s]" % (place['name'], place['color']))
                if place['area'].contains(iss):
                    curr_place = place

            # Report results
            if curr_place:
                being_controlled = True
                light.color(curr_place['color'])
                print("The ISS is over %s right now." % (curr_place['name']))
            else:
                # if we control light, then reset to original state/color
                if being_controlled:
                    light.reset()
                    being_controlled = False
                print("The ISS is NOT overhead right now.")
                print("https://www.google.com/maps/search/%f,+%f/@%f,%f,4z" % (iss[0], iss[1], iss[0] ,iss[1]))
        else:
            # pixel.blink((16,0,0), count=5)
            log("Error Getting ISS Location: %s" % (resp.status_code))

        time.sleep(15)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    log("--==> BEGIN <==--")

    config = None
    with open('.secrets.yml', 'r') as secrets:
        config = yaml.safe_load(secrets)

    HueLight.init(config['host'], config['token'])
    light = HueLight.get_by_name('Couch Light')

    durham = GPSArea.from_file("../data/durham.coords", reverse=True)
    nc     = GPSArea.from_file("../data/nc.coords", reverse=True)
    usa    = GPSArea.from_file("../data/usa.coords", reverse=True)

    try:
        # List of places should be largest to smallest area size-wise in the list
        iss_overhead(light, (
            {'name': "The USA",        'color': (128,128,128), 'area': usa},
            {'name': "North Carolina", 'color': (0,0,128),     'area': nc},
            {'name': "Durham",         'color': (0,128,0),     'area': durham}
        ))
    except Exception as e:
        log("Error: %s" % (e))
        light.color((255,0,0))



#
