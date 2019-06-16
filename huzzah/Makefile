install:
	ampy --port /dev/ttyUSB0 put main.py
	ampy --port /dev/ttyUSB0 put pixel.py
	ampy --port /dev/ttyUSB0 put ../lib/gps_area.py
	ampy --port /dev/ttyUSB0 put ../data/durham.coords
	ampy --port /dev/ttyUSB0 put ../data/nc.coords
	ampy --port /dev/ttyUSB0 put ../data/usa.coords

boot: boot.py
	ampy --port /dev/ttyUSB0 put boot.py
