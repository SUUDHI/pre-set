from utils.distance_utils import DistanceCalculator
from utils.coordinate import Coordinate
from utils.constants import BASE_FARE, RATE_PER_KM, CANCELLATION_FEE_PERCENTAGE

class FareCalculator:
    def __init__(self):
        # Base fare in dollars
        self.base_fare = BASE_FARE
        # Cost per kilometer in dollars
        self.per_km_rate = RATE_PER_KM
        # Cost per minute in dollars
        self.per_minute_rate = 0.25
        # Minimum fare in dollars
        self.minimum_fare = BASE_FARE
        # Surge multiplier (default 1.0)
        self.surge_multiplier = 1.0
        # Cancellation fee percentage
        self.cancellation_fee_percentage = CANCELLATION_FEE_PERCENTAGE
        self.distance_calculator = DistanceCalculator()

    def calculate_fare(self, pickup: Coordinate, dropoff: Coordinate, duration_minutes: float = 0.0, surge_multiplier: float = 1.0) -> float:
        """
        Calculate the total fare for a ride based on distance and duration.
        
        Args:
            pickup (Coordinate): Pickup location
            dropoff (Coordinate): Dropoff location
            duration_minutes (float): Duration of the ride in minutes
            surge_multiplier (float): Current surge pricing multiplier
            
        Returns:
            float: Total fare amount
        """
        # Calculate distance in kilometers
        distance_km = self.distance_calculator.calculate_distance(
            Coordinate(lat=pickup.lat, lng=pickup.lng),
            Coordinate(lat=dropoff.lat, lng=dropoff.lng)
        )
        
        # Calculate base components
        distance_cost = distance_km * self.per_km_rate
        time_cost = duration_minutes * self.per_minute_rate
        
        # Calculate total fare before surge
        total_fare = self.base_fare + distance_cost + time_cost
        
        # Apply surge pricing
        total_fare *= surge_multiplier
        
        # Ensure minimum fare
        total_fare = max(total_fare, self.minimum_fare)
        
        return round(total_fare, 2)

    def calculate_cancellation_fee(self, fare: float) -> float:
        """
        Calculate the cancellation fee based on the original fare.
        
        Args:
            fare (float): Original fare amount
            
        Returns:
            float: Cancellation fee amount
        """
        return round(fare * self.cancellation_fee_percentage, 2)

    def calculate_surge_multiplier(self, demand_level: int, available_drivers: int) -> float:
        """
        Calculate surge multiplier based on demand and available drivers.
        
        Args:
            demand_level (int): Current demand level (1-5)
            available_drivers (int): Number of available drivers
            
        Returns:
            float: Surge multiplier
        """
        # Base surge calculation
        if available_drivers == 0:
            return 2.0  # Maximum surge if no drivers available
        
        # Calculate driver-to-demand ratio
        ratio = available_drivers / (demand_level * 10)
        
        # Determine surge multiplier based on ratio
        if ratio < 0.5:
            return 2.0
        elif ratio < 1.0:
            return 1.75
        elif ratio < 1.5:
            return 1.5
        elif ratio < 2.0:
            return 1.25
        else:
            return 1.0

    def get_fare_breakdown(self, pickup: Coordinate, dropoff: Coordinate, duration_minutes: float = 0.0, surge_multiplier: float = 1.0) -> dict:
        """
        Get a detailed breakdown of the fare calculation.
        
        Args:
            pickup (Coordinate): Pickup location
            dropoff (Coordinate): Dropoff location
            duration_minutes (float): Duration of the ride in minutes
            surge_multiplier (float): Current surge pricing multiplier
            
        Returns:
            dict: Detailed fare breakdown
        """
        # Calculate distance in kilometers
        distance_km = self.distance_calculator.calculate_distance(
            Coordinate(lat=pickup.lat, lng=pickup.lng),
            Coordinate(lat=dropoff.lat, lng=dropoff.lng)
        )
        
        # Calculate individual components
        base = self.base_fare
        distance_cost = distance_km * self.per_km_rate
        time_cost = duration_minutes * self.per_minute_rate
        
        # Calculate subtotal
        subtotal = base + distance_cost + time_cost
        
        # Apply surge
        surge_amount = (subtotal * surge_multiplier) - subtotal
        
        # Calculate final total
        total = max(subtotal + surge_amount, self.minimum_fare)
        
        return {
            "base_fare": round(base, 2),
            "distance_cost": round(distance_cost, 2),
            "time_cost": round(time_cost, 2),
            "subtotal": round(subtotal, 2),
            "surge_multiplier": round(surge_multiplier, 2),
            "surge_amount": round(surge_amount, 2),
            "total": round(total, 2),
            "cancellation_fee_percentage": self.cancellation_fee_percentage,
            "cancellation_fee": round(total * self.cancellation_fee_percentage, 2)
        }
