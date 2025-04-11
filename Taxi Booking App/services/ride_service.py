from utils.coordinate import Coordinate
from utils.distance import calculate_distance
from utils.fare import calculate_fare
from db_operations import ride_ops
import sqlite3

class RideService:
    def request_ride(self, data):
        try:
            ride_ops.save_ride(data)
            return {"message": "Ride requested successfully!"}, 201
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def get_ride_status(self, ride_id):
        try:
            row = ride_ops.get_ride_status_by_id(ride_id)
            if row:
                return {"ride_id": ride_id, "status": row["Status"]}, 200
            else:
                return {"error": "Ride not found"}, 404
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500


    def assign_nearest_driver(self, ride_id, pickup_lat, pickup_lng):
        try:
            # Convert pickup to Coordinate
            pickup_point = Coordinate(lat=pickup_lat, lng=pickup_lng)

            drivers = ride_ops.get_available_drivers()
            if not drivers:
                return {"error": "No available drivers found"}, 404

            # Find the nearest driver using Coordinate
            nearest_driver = min(
                drivers,
                key=lambda d: calculate_distance(
                    pickup_point,
                    Coordinate(d["Latitude"], d["Longitude"])
                )
            )
            driver_id = nearest_driver["DriverID"]

            # Get ride pickup/dropoff coordinates
            ride = ride_ops.get_ride_coordinates(ride_id)
            if not ride:
                return {"error": "Ride not found"}, 404

            if (
                ride["PickupLatitude"] is None or ride["PickupLongitude"] is None or
                ride["DropoffLatitude"] is None or ride["DropoffLongitude"] is None
            ):
                return {"error": "Ride pickup or dropoff coordinates are missing"}, 400

            # Build coordinates for fare calculation
            pickup = Coordinate(ride["PickupLatitude"], ride["PickupLongitude"])
            dropoff = Coordinate(ride["DropoffLatitude"], ride["DropoffLongitude"])

            fare = calculate_fare(pickup, dropoff)

            # Assign driver and update fare
            ride_ops.assign_driver_to_ride(driver_id, ride_id, fare)

            return {
                "message": "Driver auto-assigned successfully",
                "driver_id": driver_id
            }, 200

        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def cancel_ride(self, ride_id, reason):
        ride = ride_ops.get_fare_by_ride_id(ride_id)
        if not ride:
            return {"error": "Ride not found"}, 404

        original_fare = ride["Fare"]
        cancellation_fee = round(original_fare * 0.05, 2)

        ride_ops.update_ride_as_cancelled(ride_id, reason, cancellation_fee)

        return {
            "message": "Ride cancelled successfully.",
            "original_fare": original_fare,
            "charged_cancellation_fee": cancellation_fee
        }, 200
    