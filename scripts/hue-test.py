#!/usr/bin/env python
import os
import sys
import time
import yaml

sys.path.append(F'{sys.path[0]}/..')

from lib.hue_bridge import HueBridge
# ------------------------------------------------------------------------------
def test_light(name):
    light = bridge.get_light(name)

    # light.on(False)
    print(light.name())
    print(light.on())
    print(light.color())

    light.color((255,0,0))
    print(light.color())
    time.sleep(1)

    light.color((0,255,0))
    print(light.color())
    time.sleep(1)

    light.color((0,0,255))
    print(light.color())
    time.sleep(1)

    light.reset()

    print(light.on())
    print(light.color())
# ------------------------------------------------------------------------------
DEFAULT_LIGHT='CD1'
HOME = os.getenv('HOME')

config = None
with open(F'{HOME}/.config/iss-tracker.yml', 'r') as cfile:
    config = yaml.safe_load(cfile)

hue_cfg = config.get('hue', {})
bridge = HueBridge(hue_cfg['host'], hue_cfg['token'])

light_name = DEFAULT_LIGHT
try:
    light_name = sys.argv[1]
except Exception as e:
    print(F"Usage: {sys.argv[0]} <LIGHT_NAME>")
    print(f"...Using Default Light Name: {DEFAULT_LIGHT}\n")


test_light(light_name)










#
