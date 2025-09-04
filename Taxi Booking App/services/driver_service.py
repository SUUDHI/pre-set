from db_operations import driver_ops
from db_operations import ride_ops
from utils.jwt_handler import jwt_handler
from services.validators import DriverValidator
from services.password_service import BcryptPasswordHasher
import sqlite3
import bcrypt
import re
from datetime import datetime
from typing import Dict, Tuple, Any, List, Optional

class DriverService:
    def __init__(self):
        self.validator = DriverValidator()
        self.password_hasher = BcryptPasswordHasher()
        self.email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_regex = re.compile(r'^\+?1?\d{9,15}$')

    def validate_driver_data(self, data):
        # Validate email format
        if not self.email_regex.match(data.get('email', '')):
            return False, "Invalid email format"
        
        # Validate phone format
        if not self.phone_regex.match(data.get('phone', '')):
            return False, "Invalid phone number format"
        
        # Validate password length
        if len(data.get('password', '')) < 8:
            return False, "Password must be at least 8 characters long"
        
        return True, ""

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_driver(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        try:
            # Validate driver data
            is_valid, error_message = self.validator.validate(data)
            if not is_valid:
                return {"error": error_message}, 400

            # Check if email or phone already exists
            if driver_ops.get_driver_by_email(data['email']):
                return {"error": "Email already registered"}, 400
            
            if driver_ops.get_driver_by_phone(data['phone']):
                return {"error": "Phone number already registered"}, 400

            # Check required driver fields
            if not data.get('licensePlate'):
                return {"error": "License plate is required"}, 400

            # Convert camelCase to snake_case for database operations
            data['license_plate'] = data['licensePlate']
            if 'licenseNumber' in data:
                data['license_number'] = data['licenseNumber']
            if 'vehicleType' in data:
                data['vehicle_type'] = data['vehicleType']

            # Check if license plate already exists
            if driver_ops.get_driver_by_license_plate(data['license_plate']):
                return {"error": "License plate already registered"}, 400

            # Hash password
            data['password'] = self.password_hasher.hash_password(data['password'])

            # Save driver
            driver_ops.save_driver(data)
            return {"message": "Driver registered successfully!"}, 201

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                if "Drivers.Email" in str(e):
                    return {"error": "Email already registered"}, 400
                elif "Drivers.Phone" in str(e):
                    return {"error": "Phone number already registered"}, 400
                elif "Driver.LicensePlate" in str(e):
                    return {"error": "License plate already registered"}, 400
                elif "Driver.LicenseNumber" in str(e):
                    return {"error": "License number already registered"}, 400
            return {"error": f"Integrity error: {str(e)}"}, 400
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def login_driver(self, email: str, password: str) -> Tuple[Dict[str, Any], int]:
        try:
            driver = driver_ops.get_driver_by_email(email)
            if not driver:
                return {"error": "Invalid credentials"}, 401

            # Verify password
            if not self.password_hasher.verify_password(password, driver['Password']):
                return {"error": "Invalid credentials"}, 401

            # Verify role
            if driver["Role"] != "driver":
                return {"error": "This email is not registered as a driver"}, 401

            # Generate token using the new jwt_handler
            payload = {
                "user_id": driver["UserID"],
                "role": "driver"
            }
            token = jwt_handler.generate_token(payload)
            return {"token": token, "driver": {
                "id": driver["UserID"],
                "name": driver["Name"],
                "email": driver["Email"],
                "license_plate": driver["LicensePlate"],
                "vehicle_type": driver["VehicleTypeID"]
            }}, 200

        except Exception as e:
            return {"error": f"Login error: {str(e)}"}, 500

    def validate_phone(self, phone):
        """
        Validate phone number format and convert to integer.
        """
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', str(phone))
        
        # Check if it's a valid length (assuming 10 digits for standard phone numbers)
        if len(phone) != 10:
            raise ValueError("Phone number must be 10 digits")
        
        return int(phone)

    def validate_date_of_birth(self, date_str):
        """
        Validate date of birth format and convert to YYYY-MM-DD.
        """
        try:
            # Try to parse the date in various formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']:
                try:
                    date = datetime.strptime(date_str, fmt)
                    # Check if the person is at least 18 years old
                    if (datetime.now() - date).days < 365 * 18:
                        raise ValueError("Driver must be at least 18 years old")
                    return date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")
        except Exception as e:
            raise ValueError(f"Invalid date of birth: {str(e)}")

    def update_location(self, driver_id: int, latitude: float, longitude: float) -> Tuple[Dict[str, Any], int]:
        try:
            driver_ops.update_driver_location(driver_id, latitude, longitude)
            return {"message": "Location updated successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to update location: {str(e)}"}, 500

    def update_status(self, driver_id: int, status: str) -> Tuple[Dict[str, Any], int]:
        try:
            valid_statuses = ['available', 'busy', 'offline']
            if status not in valid_statuses:
                return {"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}, 400

            driver_ops.update_driver_status(driver_id, status)
            return {"message": "Status updated successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to update status: {str(e)}"}, 500

    def get_available_drivers(self, latitude: float, longitude: float, radius: float) -> Tuple[List[Dict[str, Any]], int]:
        try:
            drivers = driver_ops.get_nearby_available_drivers(latitude, longitude, radius)
            return drivers, 200
        except Exception as e:
            return [], 500

    def get_requested_rides(self, driver_id: int) -> Tuple[List[Dict[str, Any]], int]:
        try:
            # Get driver's info
            driver = driver_ops.get_driver_by_id(driver_id)
            if not driver:
                return {"error": "Driver not found"}, 404

            # Only show ride requests if driver is available
            if driver['StatusName'].lower() != 'available':
                return [], 200

            # Get ride requests matching the driver's vehicle type
            rides = driver_ops.get_ride_requests_by_vehicle_type(driver_id, driver['VehicleTypeID'])
            return rides, 200
        except Exception as e:
            return {"error": f"Failed to get ride requests: {str(e)}"}, 500

    def accept_ride(self, driver_id: int, ride_id: int) -> Tuple[Dict[str, Any], int]:
        try:
            # Check if driver is available
            driver = driver_ops.get_driver_by_id(driver_id)
            if not driver or driver['StatusName'] != 'available':
                return {"error": "Driver is not available"}, 400

            # Check if ride is still in requested status
            ride = ride_ops.get_ride_by_id(ride_id)
            if not ride:
                return {"error": "Ride not found"}, 404
            
            if ride['Status'] != 'requested':
                return {"error": "Ride is no longer available"}, 400

            if ride['DriverID'] is not None:
                return {"error": "Ride already assigned to a driver"}, 400

            # Update ride with driver and change status
            ride_ops.assign_driver_to_ride(ride_id, driver_id)
            ride_ops.update_ride_status(ride_id, "accepted")
            
            # Update driver status to busy
            driver_ops.update_driver_status(driver_id, "busy")

            return {"message": "Ride accepted successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to accept ride: {str(e)}"}, 500

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
            
            # Verify the ride is in progress
            if ride['Status'] != 'in_progress':
                return {"error": "Only in-progress rides can be completed"}, 400
            
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
