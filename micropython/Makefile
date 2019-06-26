MAC_PORT = "/dev/tty.SLAB_USBtoUART"
LNX_PORT = "/dev/ttyUSB0"
PORT = $(MAC_PORT)

test:
	echo $(PORT)

install: boot main lib other data

boot: boot.py
	ampy --port $(PORT) put boot.py

main: main.py
	ampy --port $(PORT) put main.py

lib:
	ampy --port $(PORT) put ../lib/gps_area.py

other:
	ampy --port $(PORT) put pixel.py

data:
	ampy --port $(PORT) put ../data/durham.coords
	ampy --port $(PORT) put ../data/nc.coords
	ampy --port $(PORT) put ../data/usa.coords
