# import machine
# import time

# led1 = machine.Pin(0, machine.Pin.OUT)
# led2 = machine.Pin(2, machine.Pin.OUT)

# while (True):
#     led1.off()
#     led2.on()
#     time.sleep(1)
#     led1.on()
#     led2.off()
#     time.sleep(1)

# -----------------------------------------------------------------------------

from machine import Pin
from neopixel import NeoPixel

import random
import time

pin = Pin(15, Pin.OUT)
np = NeoPixel(pin, 1)

np[0] = (0, 0, 128)
np.write()
time.sleep(5)

for i in range(0, 100):
    np[0] = (0, 192, 0)
    np.write()
    time.sleep(random.getrandbits(3))

    np[0] = (192, 192, 0)
    np.write()
    time.sleep(random.getrandbits(3))

    np[0] = (192, 0, 0)
    np.write()
    time.sleep(random.getrandbits(3))

np[0] = (0, 0, 128)
np.write()
