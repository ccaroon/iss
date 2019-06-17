#!/usr/bin/env python
import utime
import urequests

from pixel import Pixel
from gps_area import GPSArea

# ------------------------------------------------------------------------------
def iss_overhead():
    while (True):
        # Get ISS position
        resp = urequests.get("http://api.open-notify.org/iss-now.json")
        if resp.status_code == 200:
            data = resp.json()
            iss = (float(data['iss_position']['latitude']), float(data['iss_position']['longitude']))
        else:
            raise Exception("Error Getting ISS Location: %s" % (resp.status_code))

        is_overhead = False
        if durham.contains(iss):
            is_overhead = True
            pixel.green()
            print("The ISS is over Durham right now.")

        if nc.contains(iss):
            pixel.blue()
            is_overhead = True
            print("The ISS is over North Carolina right now.")

        if usa.contains(iss):
            pixel.white()
            is_overhead = True
            print("The ISS is over the USA right now.")

        if not is_overhead:
            pixel.red(32)
            print("The ISS is NOT overhead right now.")
            print("https://www.google.com/maps/search/%f,+%f/@%f,%f,4z" % (iss[0], iss[1], iss[0] ,iss[1]))

        utime.sleep(10)

# ------------------------------------------------------------------------------
def pixel_test():
    while True:
        pixel.white()
        print("White")
        utime.sleep(1)

        pixel.red()
        print("Red")
        utime.sleep(1)

        pixel.blue()
        print("Blue")
        utime.sleep(1)

        pixel.green()
        print("Green")
        utime.sleep(1)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    pixel = Pixel(15)
    pixel.off()
    my_house = (35.922978, -78.902671)

    durham = GPSArea.from_file("./durham.coords", reverse=True)
    nc = GPSArea.from_file("./nc.coords", reverse=True)
    usa = GPSArea.from_file("./usa.coords", reverse=True)

    iss_overhead()
