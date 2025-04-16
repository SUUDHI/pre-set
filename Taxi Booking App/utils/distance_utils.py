import math
from dataclasses import dataclass
from typing import List, Tuple
from utils.coordinate import Coordinate  # Changed to use the correct Coordinate class

@dataclass
class DistanceCalculator:
    @staticmethod
    def calculate_distance(point1: Coordinate, point2: Coordinate) -> float:
        """
        Calculate the distance between two points using the Haversine formula.
        Returns distance in kilometers.
        """
        # Convert decimal degrees to radians
        lat1, lon1 = map(math.radians, [point1.lat, point1.lng])
        lat2, lon2 = map(math.radians, [point2.lat, point2.lng])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r

@dataclass
class ETAFormatter:
    @staticmethod
    def format_time(hours: float) -> str:
        """
        Format time in hours to a human-readable string.
        """
        total_minutes = hours * 60
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

@dataclass
class ETACalculator:
    def __init__(self, average_speed_kmh: float = 30.0):
        self.average_speed = average_speed_kmh
        self.distance_calculator = DistanceCalculator()
        self.time_formatter = ETAFormatter()

    def calculate_eta(self, distance_km: float) -> Tuple[float, str]:
        """
        Calculate ETA based on distance and average speed.
        Returns tuple of (hours, formatted_time_string)
        """
        time_hours = distance_km / self.average_speed
        return time_hours, self.time_formatter.format_time(time_hours)

@dataclass
class RouteCalculator:
    def __init__(self):
        self.distance_calculator = DistanceCalculator()

    def calculate_route_distance(self, coordinates: List[Coordinate]) -> float:
        """
        Calculate the total distance of a route with multiple waypoints.
        """
        total_distance = 0.0
        
        for i in range(len(coordinates) - 1):
            total_distance += self.distance_calculator.calculate_distance(
                coordinates[i], coordinates[i + 1]
            )
        
        return total_distance

@dataclass
class Geocoder:
    def get_coordinates(self, address: str) -> Coordinate:
        """
        Get coordinates from an address.
        This is a placeholder - in production, use a geocoding service.
        """
        # Placeholder implementation
        return Coordinate(0.0, 0.0)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points using the Haversine formula.
    
    Args:
        lat1 (float): Latitude of first point
        lon1 (float): Longitude of first point
        lat2 (float): Latitude of second point
        lon2 (float): Longitude of second point
        
    Returns:
        float: Distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def calculate_eta(distance_km: float, traffic_factor: float = 1.0) -> int:
    """
    Calculate estimated time of arrival based on distance and traffic conditions.
    
    Args:
        distance_km (float): Distance in kilometers
        traffic_factor (float): Traffic multiplier (1.0 = normal, >1.0 = heavy traffic)
        
    Returns:
        int: Estimated time in minutes
    """
    # Average speed in km/h (assuming 40 km/h as base speed)
    average_speed = 40
    
    # Calculate base time in hours
    time_hours = distance_km / average_speed
    
    # Apply traffic factor
    time_hours *= traffic_factor
    
    # Convert to minutes and round to nearest integer
    return round(time_hours * 60)

def get_coordinates_from_address(address: str) -> Tuple[float, float]:
    """
    Get latitude and longitude coordinates from an address.
    This is a placeholder function - in production, you would use a geocoding service.
    
    Args:
        address (str): Address string
        
    Returns:
        Tuple[float, float]: (latitude, longitude)
    """
    # This is a placeholder - in production, you would use a geocoding service
    # like Google Maps Geocoding API or OpenStreetMap Nominatim
    return (0.0, 0.0)

def calculate_route_distance(coordinates: list) -> float:
    """
    Calculate the total distance of a route with multiple waypoints.
    
    Args:
        coordinates (list): List of (latitude, longitude) tuples
        
    Returns:
        float: Total distance in kilometers
    """
    total_distance = 0.0
    
    for i in range(len(coordinates) - 1):
        lat1, lon1 = coordinates[i]
        lat2, lon2 = coordinates[i + 1]
        total_distance += calculate_distance(lat1, lon1, lat2, lon2)
    
    return total_distance 