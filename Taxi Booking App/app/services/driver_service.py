from typing import Tuple, Dict, Any

class DriverService:
    def complete_ride(self, driver_id: int, ride_id: int, dropoff_lat: float, dropoff_lon: float) -> Tuple[Dict[str, Any], int]:
        """
        Complete a ride by updating its status and setting the dropoff location.
        
        Args:
            driver_id (int): ID of the driver completing the ride
            ride_id (int): ID of the ride to complete
            dropoff_lat (float): Final dropoff latitude
            dropoff_lon (float): Final dropoff longitude
            
        Returns:
            Tuple[Dict[str, Any], int]: Response message and status code
        """
        try:
            # Get the ride details
            ride = ride_ops.get_ride_by_id(ride_id)
            if not ride:
                return {"error": "Ride not found"}, 404
            
            # Verify the ride belongs to this driver
            if ride['DriverID'] != driver_id:
                return {"error": "This ride is not assigned to you"}, 403
            
            # Verify the ride is in accepted or in progress state
            if ride['Status'] not in ['accepted', 'in_progress']:
                return {"error": "Only accepted or in-progress rides can be completed"}, 400
            
            # Update ride status to completed and set dropoff time
            ride_ops.update_dropoff_time(ride_id)
            
            # Update driver's status to available
            driver_ops.update_driver_status(driver_id, "available")
            
            # Update driver's location as the dropoff point
            driver_ops.update_driver_location(driver_id, dropoff_lat, dropoff_lon)
            
            return {
                "message": "Ride completed successfully",
                "ride_id": ride_id,
                "dropoff_location": {
                    "latitude": dropoff_lat,
                    "longitude": dropoff_lon
                }
            }, 200
            
        except Exception as e:
            return {"error": f"Failed to complete ride: {str(e)}"}, 500 