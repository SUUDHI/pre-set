from utils.coordinate import Coordinate
from utils.distance import calculate_distance
from utils.fare_config import BASE_FARE, RATE_PER_KM

def calculate_fare(pickup: Coordinate, dropoff: Coordinate) -> float:
    distance = calculate_distance(pickup, dropoff)
    fare = BASE_FARE + (distance * RATE_PER_KM)
    return round(fare, 2)
