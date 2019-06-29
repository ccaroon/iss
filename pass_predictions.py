#!/usr/bin/env python
import requests
import time

drm = (35.9230597,-78.9028224)
onc = (35.0318361,-76.69763)
miami = (25.7825452,-80.2996701)
lego_land = (33.1261476,-117.313742)
sao_palo = (-23.6815303,-46.87617)

place = onc
resp = requests.get(F"http://api.open-notify.org/iss-pass.json?lat={place[0]}&lon={place[1]}")

if resp.status_code == 200:
    data = resp.json()['response']
    for p in data:
        print(F"{time.ctime(p['risetime'])}: {p['duration']}s")
else:
    print(F"Error: {resp.status_code}")
