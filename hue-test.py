#!/usr/bin/env python
import os
import time
import yaml

from lib.hue_bridge import HueBridge

HOME = os.getenv('HOME')
config = None
with open(F'{HOME}/.config/iss-hue.yml', 'r') as cfile:
    config = yaml.safe_load(cfile)

hue = HueBridge(config['host'], config['token'])

# ------------------------------------------------------------------------------
def test_desk_light():
    light = hue.get_light("CD1")

    print(light.initial_state)

    # print(light.brightness())
    light.brightness(100)
    # print(light.brightness())

    input("Hit Any Key")

    light.reload()
    print(light.initial_state)
# ------------------------------------------------------------------------------
def test_couch_light():
    light = hue.get_light('Couch Light')

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
test_desk_light()
