#!/usr/bin/env python
import time
import yaml

from hue_light import HueLight

config = None
with open('.secrets.yml', 'r') as secrets:
    config = yaml.safe_load(secrets)

HueLight.init(config['host'], config['token'])
light = HueLight.get_by_name('Couch Light')

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
