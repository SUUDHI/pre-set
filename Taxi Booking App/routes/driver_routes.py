from flask import Blueprint, request, jsonify, g
from services.driver_service import DriverService
from services.validators import DriverValidator
from utils.jwt_handler import jwt_handler
from db.connect_db import DatabaseConnector
from utils.auth import token_required
from db_operations.driver_ops import DriverOps

driver_bp = Blueprint("driver", __name__)
driver_service = DriverService()
driver_validator = DriverValidator()
driver_ops = DriverOps()

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

@driver_bp.route("/status", methods=["GET"])
@jwt_handler.token_required(role="driver")
def get_driver_status():
    try:
        driver_id = g.user_id
        if not driver_id:
            return jsonify({'error': 'Invalid driver credentials'}), 401
            
        status = driver_ops.get_driver_status(driver_id)
        
        if status is None:
            return jsonify({'error': 'Driver not found'}), 404
            
        return jsonify({
            'status': status,
            'driver_id': driver_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@driver_bp.route("/status", methods=["PUT"])
@jwt_handler.token_required(role="driver")
def update_driver_status():
    try:
        driver_id = g.user_id
        if not driver_id:
            return jsonify({'error': 'Invalid driver credentials'}), 401
            
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
            
        new_status = data['status'].upper()
        valid_statuses = ['AVAILABLE', 'BUSY', 'OFFLINE']
        
        if new_status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400

        driver_ops.update_driver_status(driver_id, new_status)
        
        return jsonify({
            'message': 'Status updated successfully',
            'status': new_status,
            'driver_id': driver_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@driver_bp.route("/vehicle-types", methods=["GET"])
def get_vehicle_types():
    """Get all available vehicle types"""
    try:
        conn = DatabaseConnector.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                VehicleTypeID,
                Name,
                Description,
                BaseRate,
                PricePerKm,
                MaxPassengers
            FROM VehicleTypes
            ORDER BY BaseRate ASC
        """)
        
        vehicle_types = []
        for row in cursor.fetchall():
            vehicle_types.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'baseRate': row[3],
                'pricePerKm': row[4],
                'maxPassengers': row[5]
            })
            
        return jsonify(vehicle_types), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()