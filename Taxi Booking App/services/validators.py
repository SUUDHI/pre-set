import re
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, Any, List

class DataValidator(ABC):
    @abstractmethod
    def validate(self, data: dict) -> tuple[bool, str]:
        pass

class BaseValidator(DataValidator):
    def __init__(self):
        self.email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_regex = re.compile(r'^\+?1?\d{9,15}$')

    def validate_required_fields(self, data: dict, required_fields: List[str]) -> Tuple[bool, str]:
        """Generic validator for checking presence and non-empty values of required fields."""
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing or empty required field: {field}"
        return True, ""

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """Validate email format."""
        if not self.email_regex.match(email):
            return False, "Invalid email format"
        return True, ""

    def validate_phone(self, phone: str) -> Tuple[bool, str]:
        """Validate phone format."""
        if not self.phone_regex.match(phone):
            return False, "Invalid phone number format"
        return True, ""

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password requirements."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        return True, ""

class UserValidator(BaseValidator):
    def validate(self, data: dict) -> Tuple[bool, str]:
        # Check required fields
        required_fields = ["name", "email", "phone", "password", "role"]
        is_valid, message = self.validate_required_fields(data, required_fields)
        if not is_valid:
            return False, message

        # Validate email
        is_valid, message = self.validate_email(data.get('email', ''))
        if not is_valid:
            return False, message

        # Validate phone
        is_valid, message = self.validate_phone(data.get('phone', ''))
        if not is_valid:
            return False, message

        # Validate password
        is_valid, message = self.validate_password(data.get('password', ''))
        if not is_valid:
            return False, message

        return True, ""

class DriverValidator(UserValidator):
    def validate(self, data: dict) -> Tuple[bool, str]:
        # First validate common user data
        is_valid, message = super().validate(data)
        if not is_valid:
            return False, message

        # Validate driver-specific fields
        if not data.get('licensePlate'):
            return False, "License plate is required"

        # Validate date of birth
        if not self._validate_date_of_birth(data.get('birth')):
            return False, "Driver must be at least 18 years old"

        return True, ""

    def _validate_date_of_birth(self, date_str: str) -> bool:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return (datetime.now() - date).days >= 365 * 18
        except (ValueError, TypeError):
            return False

class RideValidator(BaseValidator):
    def validate(self, data: dict) -> Tuple[bool, str]:
        required_fields = ["pickup_lat", "pickup_lon", "dropoff_lat", "dropoff_lon"]
        return self.validate_required_fields(data, required_fields)

class LocationValidator(BaseValidator):
    def validate(self, data: dict) -> Tuple[bool, str]:
        required_fields = ["latitude", "longitude"]
        return self.validate_required_fields(data, required_fields)

class PhoneValidator:
    @staticmethod
    def validate_and_format(phone: str) -> str:
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', str(phone))
        
        # Check if it's a valid length
        if len(phone) != 10:
            raise ValueError("Phone number must be 10 digits")
        
        return phone 