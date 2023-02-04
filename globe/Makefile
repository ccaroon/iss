MAC_PORT = "/dev/tty.SLAB_USBtoUART"
LNX_PORT = "/dev/ttyUSB0"
PORT = $(LNX_PORT)

test:
	echo $(PORT)

install: boot main libs data

boot:
	ampy --port $(PORT) put boot.py

main:
	ampy --port $(PORT) put main.py

libs:
	ampy --port $(PORT) put ../lib/gps_area.py
	ampy --port $(PORT) put lib/pixel.py
	ampy --port $(PORT) put lib/secrets.py
	ampy --port $(PORT) put lib/wifi.py

data:
	ampy --port $(PORT) put ../data/durham.coords
	ampy --port $(PORT) put ../data/nc.coords
	ampy --port $(PORT) put ../data/usa.coords

shell:
	picocom $(PORT) -b115200

log:
	ampy --port $(PORT) get iss.log
