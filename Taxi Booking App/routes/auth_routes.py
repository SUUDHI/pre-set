# routes/auth_routes.py

from flask import Blueprint, request, jsonify, render_template
from services.auth_service import AuthService
from services.driver_service import DriverService
from utils.jwt_handler import generate_token

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()
driver_service = DriverService()

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
    
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        response, status = auth_service.login_user(data["email"], data["password"])
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
