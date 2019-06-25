#!/usr/bin/env python
import os
import requests
import time

from lib.gps_area import GPSArea

MAC_ALERT = os.path.expanduser("~/bin/mac-alert.sh")

# ------------------------------------------------------------------------------
def notify(title, msg):
    print(F"--- {title} ---")
    print(msg)
    if os.path.exists(MAC_ALERT):
        os.system("%s '%s' '%s'" % (MAC_ALERT, title, msg))

# ------------------------------------------------------------------------------
def iss_overhead(places):
    while (True):
        # Get ISS position
        resp = requests.get("http://api.open-notify.org/iss-now.json")
        if resp.status_code == 200:
            data = resp.json()
            iss = (float(data['iss_position']['latitude']), float(data['iss_position']['longitude']))
        else:
            raise Exception("Error Getting ISS Location: %s" % (resp.status_code))

        # Check list of places
        curr_place = None
        for place in places:
            if place['area'].contains(iss):
                curr_place = place

        # Report results
        if curr_place:
            msg = "The ISS is over %s right now." % (curr_place['name'])
            notify("ISS", msg)
        else:
            print("The ISS is NOT overhead right now.")
            print("https://www.google.com/maps/search/%f,+%f/@%f,%f,4z" % (iss[0], iss[1], iss[0] ,iss[1]))

        time.sleep(15)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    durham = GPSArea.from_file("./data/durham.coords", reverse=True)
    nc     = GPSArea.from_file("./data/nc.coords", reverse=True)
    usa    = GPSArea.from_file("./data/usa.coords", reverse=True)

    # List of places should be largest to smallest area size-wise in the list
    iss_overhead((
        {'name': "The USA",        'area': durham},
        {'name': "North Carolina", 'area': nc},
        {'name': "Durham",         'area': durham}
    ))
