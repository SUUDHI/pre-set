from utils.distance import calculate_distance

def calculate_fare(pickup_lat, pickup_lng, drop_lat, drop_lng):
    base_fare = 50  
    rate_per_km = 15

    distance = calculate_distance(pickup_lat, pickup_lng, drop_lat, drop_lng)
    fare = base_fare + (distance * rate_per_km)
    return round(fare, 2)
