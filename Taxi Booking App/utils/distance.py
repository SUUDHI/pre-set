from math import radians, sin, cos, sqrt, atan2
from utils.coordinate import Coordinate

def calculate_distance(start: Coordinate, end: Coordinate) -> float:
    """
    Calculates the great-circle distance between two points on the Earth's surface using the Haversine formula.
    """
    earth_radius_km = 6371  # Earth's radius in kilometers

    dlat = radians(end.lat - start.lat)
    dlng = radians(end.lng - start.lng)

    a = sin(dlat / 2)**2 + cos(radians(start.lat)) * cos(radians(end.lat)) * sin(dlng / 2)**2
    haversine_angle = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * haversine_angle
