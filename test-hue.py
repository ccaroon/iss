#!/usr/bin/env python
import time
import yaml

from lib.hue_bridge import HueBridge

config = None
with open('.secrets.yml', 'r') as secrets:
    config = yaml.safe_load(secrets)

hue = HueBridge(config['host'], config['token'])
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
