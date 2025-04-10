from math import radians, sin, cos, sqrt, atan2
from utils.coordinate import Coordinate

def calculate_distance(start: Coordinate, end: Coordinate) -> float:
    
    earth_radius_km = 6371  # Average Earth radius in kilometers

    delta_latitude = radians(end.lat - start.lat)
    delta_longitude = radians(end.lng - start.lng)

    haversine_formula_component = (
        sin(delta_latitude / 2) ** 2
        + cos(radians(start.lat)) * cos(radians(end.lat)) * sin(delta_longitude / 2) ** 2
    )

    central_angle = 2 * atan2(sqrt(haversine_formula_component), sqrt(1 - haversine_formula_component))

    distance_in_kilometers = earth_radius_km * central_angle
    return distance_in_kilometers
