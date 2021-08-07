from abc import ABC, abstractmethod
class LocationHandler(ABC):

    def __init__(self, name, config):
        self._name = name
        self._config = config

    @abstractmethod
    # Called when the location of the ISS changes.
    def location(self, long_lat):
        raise NotImplementedError("'location' is an Abstract Method and must be overridden.")

    @abstractmethod
    # Called when the ISS is over a known/monitored place
    # * 'place' can be None to indicate that it's no longer over a known_place
    def known_place(self, place):
        raise NotImplementedError("'known_place' is an Abstract Method and must be overridden.")

    @abstractmethod
    # Called when the ISS is over a known/monitored place
    def error(self, err_msg):
        raise NotImplementedError("'error' is an Abstract Method and must be overridden.")

    def log(self, msg):
        print(F"{self._name} - {msg}")
