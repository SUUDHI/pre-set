# ✅ services/auth_service.py
from db_operations import user_ops
from utils.jwt_handler import jwt_handler
from services.validators import UserValidator
from services.password_service import BcryptPasswordHasher
import sqlite3
import bcrypt
import re
from typing import Dict, Tuple, Any

class AuthService:
    def __init__(self):
        self.email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_regex = re.compile(r'^\+?1?\d{9,15}$')
        self.validator = UserValidator()
        self.password_hasher = BcryptPasswordHasher()

    def validate_user_data(self, data):
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

    def register_user(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        try:
            # Validate user data
            is_valid, error_message = self.validator.validate(data)
            if not is_valid:
                return {"error": error_message}, 400

            # Check if email or phone already exists
            if user_ops.get_user_by_email(data['email']):
                return {"error": "Email already registered"}, 400
            
            if user_ops.get_user_by_phone(data['phone']):
                return {"error": "Phone number already registered"}, 400

            # Hash password
            data['password'] = self.password_hasher.hash_password(data['password'])

            # Save user
            user_ops.save_user(data)
            return {"message": f"{data['role'].capitalize()} registered successfully!"}, 201

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                if "Users.Email" in str(e):
                    return {"error": "Email already registered"}, 400
                elif "Users.Phone" in str(e):
                    return {"error": "Phone number already registered"}, 400
            return {"error": f"Integrity error: {str(e)}"}, 400
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def login_user(self, email: str, password: str, role: str) -> Tuple[Dict[str, Any], int]:
        try:
            user = user_ops.get_user_by_email(email)
            if not user:
                return {"error": "Invalid credentials"}, 401

            # Verify password
            if not self.password_hasher.verify_password(password, user['Password']):
                return {"error": "Invalid credentials"}, 401

            # Verify role
            if user["Role"] != role:
                return {"error": f"This email is registered as a {user['Role']}, not as a {role}"}, 401

            # Generate token using the new jwt_handler
            payload = {
                "user_id": user["UserID"],
                "role": user["Role"]
            }
            token = jwt_handler.generate_token(payload)
            return {"token": token, "user": {
                "id": user["UserID"],
                "name": user["Name"],
                "email": user["Email"],
                "role": user["Role"]
            }}, 200

        except Exception as e:
            return {"error": f"Login error: {str(e)}"}, 500
