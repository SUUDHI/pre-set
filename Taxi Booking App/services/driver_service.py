from db_operations import driver_ops
from db_operations import ride_ops
from utils.jwt_utils import generate_token
import sqlite3
import bcrypt
import re
from datetime import datetime

class DriverService:
    def __init__(self):
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

    def register_driver(self, data):
        try:
            # Validate driver data
            is_valid, error_message = self.validate_driver_data(data)
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
            data['password'] = self.hash_password(data['password']).decode('utf-8')

            # Save driver
            result = driver_ops.save_driver(data)
            return {"success": True, "message": "Driver registered successfully!"}, 201

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                if "Users.Email" in str(e):
                    return {"error": "Email already registered"}, 400
                elif "Users.Phone" in str(e):
                    return {"error": "Phone number already registered"}, 400
                elif "Driver.LicensePlate" in str(e):
                    return {"error": "License plate already registered"}, 400
                elif "Driver.LicenseNumber" in str(e):
                    return {"error": "License number already registered"}, 400
            return {"error": f"Database error: {str(e)}"}, 400
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def login_driver(self, email, password):
        try:
            driver = driver_ops.get_driver_by_credentials(email, password)
            if not driver:
                return {"error": "Invalid credentials"}, 401

            # Generate token
            payload = {
                "user_id": driver["UserID"],
                "role": "driver"
            }
            token = generate_token(payload)
            return {"token": token, "driver": {
                "id": driver["UserID"],
                "name": driver["Name"],
                "email": driver["Email"],
                "license_plate": driver["LicensePlate"]
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

    def update_location(self, driver_id, latitude, longitude):
        """
        Update driver's real-time location.
        """
        try:
            driver_ops.update_driver_location(driver_id, latitude, longitude)
            return {"message": "Location updated successfully"}, 200
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def update_status(self, driver_id, status):
        """
        Update driver's status (available, busy, offline).
        """
        try:
            if status not in ["available", "busy", "offline"]:
                return {"error": "Invalid status"}, 400
            
            driver_ops.update_driver_status(driver_id, status)
            return {"message": f"Status updated to {status}"}, 200
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def get_available_drivers(self):
        """
        Get all available drivers.
        """
        try:
            drivers = driver_ops.get_available_drivers()
            return {
                "drivers": [dict(driver) for driver in drivers]
            }, 200
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def accept_ride(self, ride_id: int, driver_id: int) -> tuple[dict, int]:
        """
        Accept a ride request.
        
        Args:
            ride_id (int): ID of the ride to accept
            driver_id (int): ID of the driver accepting the ride
            
        Returns:
            tuple[dict, int]: Response message and status code
        """
        try:
            # Check if driver is available
            driver = driver_ops.get_driver_by_id(driver_id)
            if not driver:
                return {"error": "Driver not found"}, 404
                
            if driver.get('StatusName') != 'available':
                return {"error": "Driver must be available to accept rides"}, 400
            
            # Check if ride exists and is in 'requested' status
            ride = ride_ops.get_ride_by_id(ride_id)
            if not ride:
                return {"error": "Ride not found"}, 404
                
            if ride.get('Status') != 'requested':
                return {"error": "Ride is not in requested status"}, 400
                
            if ride.get('DriverID') is not None:
                return {"error": "Ride already assigned to a driver"}, 400
            
            # Update ride with driver and change status to 'accepted'
            ride_ops.assign_driver_to_ride(ride_id, driver_id)
            ride_ops.update_ride_status(ride_id, "accepted")
            
            # Update driver status to busy
            driver_ops.update_driver_status(driver_id, "busy")
            
            return {
                "message": "Ride accepted successfully",
                "ride_id": ride_id,
                "driver_id": driver_id,
                "status": "accepted"
            }, 200
            
        except Exception as e:
            return {"error": f"Failed to accept ride: {str(e)}"}, 500
