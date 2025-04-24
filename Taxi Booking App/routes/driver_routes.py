from flask import Blueprint, request, jsonify, g
from services.driver_service import DriverService
from services.validators import DriverValidator
from utils.jwt_handler import jwt_handler

driver_bp = Blueprint("driver", __name__)
driver_service = DriverService()
driver_validator = DriverValidator()

@driver_bp.route("/register", methods=["POST"])
def register_driver():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    is_valid, message = driver_validator.validate(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    response, status = driver_service.register_driver(data)
    return jsonify(response), status

@driver_bp.route("/login", methods=["POST"])
def login_driver():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    response, status = driver_service.login_driver(email, password)
    return jsonify(response), status

@driver_bp.route("/location", methods=["PUT"])
@jwt_handler.token_required(role="driver")
def update_driver_location():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    response, status = driver_service.update_location(g.user_id, latitude, longitude)
    return jsonify(response), status

@driver_bp.route("/status", methods=["PUT"])
@jwt_handler.token_required(role="driver")
def update_driver_status():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    status = data.get("status")
    if not status:
        return jsonify({"error": "Status is required"}), 400
        
    if status not in ["available", "busy", "offline"]:
        return jsonify({"error": "Invalid status. Must be one of: available, busy, offline"}), 400

    response, status_code = driver_service.update_status(g.user_id, status)
    return jsonify(response), status_code

@driver_bp.route("/rides/<int:ride_id>/accept", methods=["POST"])
@jwt_handler.token_required(role="driver")
def accept_ride(ride_id):
    """Accept a ride request by a driver"""
    try:
        # Get driver ID from the token
        driver_id = g.user_id
        
        response, status = driver_service.accept_ride(driver_id, ride_id)
        return jsonify(response), status
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@driver_bp.route("/rides/requested", methods=["GET"])
@jwt_handler.token_required(role="driver")
def get_requested_rides():
    """Get all available ride requests"""
    try:
        response, status = driver_service.get_requested_rides(g.user_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500