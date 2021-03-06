from math import sin, asin, cos, sqrt, radians

# distance in kilometers between two positions
# position is given as spherical coordinates (lat, lon)

# the last factor is an approximation to the street network
# TODO: Query google maps for realistic times


def get_distance(a, b):
    lat1, lon1 = a.lat, a.lon
    lat2, lon2 = b.lat, b.lon
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(a)) * 1.4
