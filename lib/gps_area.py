import math

class GPSArea:
    # pts - list of tuples; each tuple == (lat, lng)
    def __init__(self, pts):
        self.__latitudes = []
        self.__longitudes = []

        if len(pts) < 3:
            raise ValueError("Must provide at least 3 sets of coordinates.")

        for coord in pts:
            self.__latitudes.append(coord[0])
            self.__longitudes.append(coord[1])

        if len(self.__latitudes) != len(self.__longitudes):
            raise ValueError("Unbalanced coordinate set. Number of latitudes and longitudes must match.")

    def contains(self, coords):
        in_area = False
        latitude = coords[0]
        longitude = coords[1]
        num_coords = len(self.__latitudes)

        angle = 0
        for i in range(0, num_coords):
            point1_lat = self.__latitudes[i] - latitude
            point1_long = self.__longitudes[i] - longitude

            point2_lat = self.__latitudes[(i + 1) % num_coords] - latitude
            point2_long = self.__longitudes[(i + 1) % num_coords] - longitude

            angle += self.angle_2d(point1_lat, point1_long, point2_lat, point2_long)

        if math.fabs(angle) >= math.pi:
            in_area = True

        return in_area

    def angle_2d(self, y1, x1, y2, x2):
        theta1 = math.atan2(y1, x1)
        theta2 = math.atan2(y2, x2)
        dtheta = theta2 - theta1

        while (dtheta > math.pi):
            dtheta -= (math.pi * 2)

        while (dtheta < -math.pi):
            dtheta += (math.pi * 2)

        return (dtheta)

    def __str__(self):
        return "[%f, %f]" % (self.__latitudes[0], self.__longitudes[0])

    @classmethod
    # Assumes that the given file contains a list of lat,lng pairs, one per line
    def from_file(cls, filename, reverse=False):
        with open(filename, "r") as file:
            coords = []
            for line in file:
                (lat, lng) = line.rstrip().split(',', 2)
                if reverse:
                    (lng, lat) = (lat, lng)
                coords.append((float(lat), float(lng)))

        return (cls(coords))

    @staticmethod
    def is_valid_coordinate(latitude, longitude):
        valid = False

        if latitude > -90 and latitude < 90 and longitude > -180 and longitude < 180:
            valid = True

        return valid
