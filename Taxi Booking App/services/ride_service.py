# services/ride_service.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import sqlite3
from db.connect_db import DatabaseConnector
from utils.coordinate import Coordinate
from utils.distance_utils import ETACalculator
from utils.fare import FareCalculator
from db_operations.ride_ops import (
    save_ride,
    get_ride_status_by_id,
    get_available_drivers,
    get_ride_coordinates,
    assign_driver_to_ride,
    get_ride_by_id,
    get_fare_by_ride_id,
    update_ride_as_cancelled,
    calculate_ride_eta,
    get_ride_with_eta,
    update_ride_status
)
from datetime import datetime

class RideRepository(ABC):
    @abstractmethod
    def save_ride(self, data: dict) -> int:
        pass

    @abstractmethod
    def get_ride(self, ride_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_available_drivers(self) -> list:
        pass

class SQLiteRideRepository(RideRepository):
    def save_ride(self, data: dict) -> int:
        return save_ride(data)

    def get_ride(self, ride_id: int) -> Optional[dict]:
        return get_ride_by_id(ride_id)

    def get_available_drivers(self) -> list:
        return get_available_drivers()

@dataclass
class RideService:
    ride_repository: RideRepository
    eta_calculator: ETACalculator
    fare_calculator: FareCalculator

    def __init__(
        self,
        repository: RideRepository = None,
        eta_calc: ETACalculator = None,
        fare_calc: FareCalculator = None
    ):
        """
        Initialize RideService with its dependencies.
        Dependencies can be injected for testing or using different implementations.
        """
        self.ride_repository = repository or SQLiteRideRepository()
        self.eta_calculator = eta_calc or ETACalculator()
        self.fare_calculator = fare_calc or FareCalculator()

    def request_ride(self, user_id: int, pickup: Coordinate, dropoff: Coordinate) -> dict:
        """
        Request a new ride.
        
        Args:
            user_id (int): ID of the user requesting the ride
            pickup (Coordinate): Pickup location
            dropoff (Coordinate): Dropoff location
            
        Returns:
            dict: Ride details including fare and ETA
        """
        try:
            # Calculate fare
            fare = self.fare_calculator.calculate_fare(pickup, dropoff)
            
            # Calculate ETA
            distance_km = self.fare_calculator.distance_calculator.calculate_distance(pickup, dropoff)
            eta_hours, eta_formatted = self.eta_calculator.calculate_eta(distance_km)
            
            # Create ride record
            ride_data = {
                "user_id": user_id,
                "pickup_lat": pickup.lat,
                "pickup_lon": pickup.lng,
                "dropoff_lat": dropoff.lat,
                "dropoff_lon": dropoff.lng,
                "fare": fare,
                "status": "requested",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            ride_id = self.ride_repository.save_ride(ride_data)
            
            return {
                "ride_id": ride_id,
                "fare": fare,
                "eta": eta_formatted,
                "status": "requested"
            }
            
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def get_ride_status(self, ride_id: int) -> dict:
        """
        Get the current status of a ride.
        
        Args:
            ride_id (int): ID of the ride
            
        Returns:
            dict: Ride status and details
        """
        try:
            print(f"RideService: Fetching ride {ride_id}")  # Debug log
            
            ride = self.ride_repository.get_ride(ride_id)
            print(f"RideService: Retrieved ride data: {ride}")  # Debug log
            
            if not ride:
                print(f"RideService: Ride {ride_id} not found")  # Debug log
                return {"error": "Ride not found"}, 404
            
            # Get status name
            status_name = ride.get('Status', 'unknown')
            
            response = {
                "ride_id": ride_id,
                "status": status_name,
                "user_id": ride.get('UserID'),
                "driver_id": ride.get('DriverID'),
                "fare": ride.get('Fare'),
                "pickup": {
                    "lat": ride.get('PickupLat'),
                    "lon": ride.get('PickupLon')
                },
                "dropoff": {
                    "lat": ride.get('DropoffLat'),
                    "lon": ride.get('DropoffLon')
                },
                "requested_at": ride.get('RequestedAt'),
                "pickup_time": ride.get('PickupTime'),
                "dropoff_time": ride.get('DropoffTime')
            }
            
            print(f"RideService: Returning response: {response}")  # Debug log
            return response
            
        except sqlite3.Error as e:
            print(f"RideService: Database error: {str(e)}")  # Debug log
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            print(f"RideService: Unexpected error: {str(e)}")  # Debug log
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def update_ride_status(self, ride_id: int, status: str) -> dict:
        """
        Update the status of a ride.
        
        Args:
            ride_id (int): ID of the ride
            status (str): New status
            
        Returns:
            dict: Updated ride details
        """
        try:
            ride_ops.update_ride_status(ride_id, status)
            return {"message": f"Ride status updated to {status}"}, 200
            
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def cancel_ride(self, ride_id: int, cancellation_reason: str, cancellation_fee: float = 0.0) -> dict:
        """
        Cancel a ride with reason and fee.
        
        Args:
            ride_id (int): ID of the ride to cancel
            cancellation_reason (str): Reason for cancellation
            cancellation_fee (float): Fee charged for cancellation
            
        Returns:
            dict: Cancellation confirmation
        """
        try:
            # First check if ride exists and get current status
            ride = self.ride_repository.get_ride(ride_id)
            if not ride:
                return {"error": "Ride not found"}, 404
                
            # Check if ride is already cancelled
            if ride.get('Status') == 'cancelled':
                return {"error": "Ride is already cancelled"}, 400
            
            # Calculate 5% of fare as cancellation fee
            fare = ride.get('Fare', 0.0)
            calculated_cancellation_fee = fare * 0.05
            
            # Update ride status with reason and fee
            update_ride_as_cancelled(ride_id, cancellation_reason, calculated_cancellation_fee)
            
            return {
                "message": "Ride cancelled successfully",
                "ride_id": ride_id,
                "cancellation_reason": cancellation_reason,
                "cancellation_fee": calculated_cancellation_fee,
                "original_fare": fare
            }, 200
            
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def assign_nearest_driver(self, ride_id: int, pickup_lat: float, pickup_lng: float) -> tuple[dict, int]:
        try:
            pickup = Coordinate(lat=pickup_lat, lng=pickup_lng)
            drivers = self.ride_repository.get_available_drivers()
            if not drivers:
                return {"error": "No available drivers found"}, 404

            nearest_driver = min(
                drivers,
                key=lambda d: self.eta_calculator.distance_calculator.calculate_distance(
                    pickup.lat, pickup.lng,
                    d["latitude"], d["longitude"]
                )
            )

            driver_id = nearest_driver["id"]
            ride = get_ride_coordinates(ride_id)

            if not ride:
                return {"error": "Ride not found"}, 404

            if any(ride[k] is None for k in ("pickup_lat", "pickup_lng", "drop_lat", "drop_lng")):
                return {"error": "Missing ride coordinates"}, 400

            fare = self.fare_calculator.calculate_fare(
                Coordinate(ride["pickup_lat"], ride["pickup_lng"]),
                Coordinate(ride["drop_lat"], ride["drop_lng"])
            )

            assign_driver_to_ride(driver_id, ride_id, fare)

            return {"message": "Driver auto-assigned successfully", "driver_id": driver_id}, 200
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def get_ride_eta(self, ride_id: int) -> tuple[dict, int]:
        try:
            ride = get_ride_with_eta(ride_id)
            if not ride:
                return {"error": "Ride not found"}, 404
            
            if 'DriverID' not in ride or not ride['DriverID']:
                return {
                    "message": "No driver assigned yet",
                    "ride_id": ride_id
                }, 200
            
            return {
                "ride_id": ride_id,
                "distance_km": ride.get('distance_km'),
                "eta_hours": ride.get('eta_hours'),
                "eta_formatted": ride.get('eta_formatted'),
                "driver_id": ride['DriverID'],
                "status": ride['Status']
            }, 200
            
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Error calculating ETA: {str(e)}"}, 500
