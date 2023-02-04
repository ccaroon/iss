#!/usr/bin/env python
import utime
import urequests

from machine import Pin

from pixel import Pixel
from gps_area import GPSArea

LOG_FILE = "iss.log"
def log(msg):
    with open(LOG_FILE, "a") as file:
        file.write("%d - %s\n" % (utime.time(), msg))

# ------------------------------------------------------------------------------
def iss_overhead(pixel, places):
    while (True):
        # Get ISS position
        resp = urequests.get("http://api.open-notify.org/iss-now.json")
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
                pixel.color(curr_place['color'])
                print("The ISS is over %s right now." % (curr_place['name']))
            else:
                pixel.blink((0,16,16), count=3)
                print("The ISS is NOT overhead right now.")
                print("https://www.google.com/maps/search/%f,+%f/@%f,%f,4z" % (iss[0], iss[1], iss[0] ,iss[1]))
        else:
            pixel.blink((16,0,0), count=5)
            log("Error Getting ISS Location: %s" % (resp.status_code))

        utime.sleep(6)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    log("--==> BEGIN <==--")
    pixel = Pixel(15)
    pixel.off()

    # blue_led = Pin(2, Pin.OUT)
    # blue_led.off() #Actually ON

    durham = GPSArea.from_file("./durham.coords", reverse=True)
    nc     = GPSArea.from_file("./nc.coords", reverse=True)
    usa    = GPSArea.from_file("./usa.coords", reverse=True)

    try:
        # List of places should be largest to smallest area size-wise in the list
        iss_overhead(pixel, (
            {'name': "The USA",        'color': (128,128,128), 'area': usa},
            {'name': "North Carolina", 'color': (0,0,128),     'area': nc},
            {'name': "Durham",         'color': (0,128,0),     'area': durham}
        ))
    except Exception as e:
        print("Error: %s" % (e))
        log("Error: %s" % (e))
        pixel.color((64,0,0))



#
