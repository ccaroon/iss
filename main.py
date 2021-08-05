#!/usr/bin/env python
import os
import yaml

from lib.blynk_handler import BlynkHandler
from lib.hue_handler import HueHandler
from lib.gps_area import GPSArea
from lib.tracker import Tracker
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    handlers = []

    config = None
    with open(F"{os.getenv('HOME')}/.config/iss-hue.yml", 'r') as cfile:
        config = yaml.safe_load(cfile)

    blynk_cfg = config.get('blynk', {})
    blynk_map = BlynkHandler('BlynkMap', blynk_cfg)
    handlers.append(blynk_map)

    hue_cfg = config.get('hue', {})
    hue_handler = HueHandler(hue_cfg['light'], hue_cfg)
    handlers.append(hue_handler)

    durham = GPSArea.from_file("./data/durham.coords", reverse=True)
    nc     = GPSArea.from_file("./data/nc.coords", reverse=True)
    usa    = GPSArea.from_file("./data/usa.coords", reverse=True)

    tracker = Tracker(
        config.get('name', 'ISS'),
        (
            {'name': "The USA",        'color': (128,128,128), 'area': usa},
            {'name': "North Carolina", 'color': (0,0,255),     'area': nc},
            {'name': "Durham",         'color': (0,255,0),     'area': durham}
        ),
        handlers
    )

    tracker.run()







#
