# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.driver_service import DriverService
from services.validators import UserValidator
from utils.jwt_handler import jwt_handler

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()
driver_service = DriverService()
user_validator = UserValidator()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    required_fields = ["name", "email", "phone", "password", "birth", "gender", "role"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        if data["role"] == "driver":
            if "licensePlate" not in data:
                return jsonify({"error": "License plate is required for drivers"}), 400
            response, status = driver_service.register_driver(data)
        else:
            response, status = auth_service.register_user(data)
        
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not data or not data.get("email") or not data.get("password") or not data.get("role"):
        return jsonify({"error": "Email, password, and role are required"}), 400
    
    try:
        if data["role"] == "driver":
            response, status = driver_service.login_driver(data["email"], data["password"])
        else:
            response, status = auth_service.login_user(data["email"], data["password"], data["role"])
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
