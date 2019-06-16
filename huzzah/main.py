#!/usr/bin/env python
import utime
import urequests
from machine import Pin

from gps_area import GPSArea

# Huzzah is backwards ... ON == OFF / OFF == ON
red_led = Pin(0, Pin.OUT)
red_led.on()
blue_led = Pin(2, Pin.OUT)
blue_led.on()

my_house = (35.922978, -78.902671)

durham = GPSArea.from_file("./durham.coords", reverse=True)
nc = GPSArea.from_file("./nc.coords", reverse=True)
usa = GPSArea.from_file("./usa.coords", reverse=True)

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
        print("The ISS is over Durham right now.")

    if nc.contains(iss):
        is_overhead = True
        print("The ISS is over North Carolina right now.")

    if usa.contains(iss):
        is_overhead = True
        print("The ISS is over the USA right now.")

    if is_overhead:
        red_led.on()
        blue_led.off()
    else:
        red_led.off()
        print("The ISS is NOT overhead right now.")
        print("https://www.google.com/maps/search/%f,+%f/@%f,%f,4z" % (iss[0], iss[1], iss[0] ,iss[1]))

    utime.sleep(7)
