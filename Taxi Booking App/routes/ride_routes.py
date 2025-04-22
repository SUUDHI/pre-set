from flask import Blueprint, request, jsonify, g
from services.ride_service import RideService
from utils.coordinate import Coordinate
from utils.jwt_handler import jwt_handler
from services.validators import RideValidator
import sqlite3
from db.connect_db import DatabaseConnector

ride_bp = Blueprint('ride', __name__)
ride_service = RideService()
ride_validator = RideValidator()

@ride_bp.route('/history', methods=['GET'])
@jwt_handler.token_required()
def get_ride_history():
    """Get ride history for the current user"""
    try:
        conn = DatabaseConnector.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                r.RideID,
                r.PickupLat,
                r.PickupLon,
                r.DropoffLat,
                r.DropoffLon,
                r.Fare,
                r.CancellationFee,
                rs.Name as Status,
                r.RequestedAt,
                r.CancellationReason
            FROM Rides r
            JOIN RideStatus rs ON r.StatusID = rs.StatusID
            WHERE r.UserID = ?
            ORDER BY r.RequestedAt DESC
        """, (g.user_id,))
        
        rides = cursor.fetchall()
        return jsonify({
            "rides": [dict(ride) for ride in rides]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ride_bp.route('/request', methods=['POST'])
@jwt_handler.token_required()
def request_ride():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400
            
        # Validate ride data using the new validator
        is_valid, error_message = ride_validator.validate(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400
        
        # Create Coordinate objects with correct attribute names
        pickup = Coordinate(
            lat=float(data['pickup_lat']),
            lng=float(data['pickup_lon'])
        )
        dropoff = Coordinate(
            lat=float(data['dropoff_lat']),
            lng=float(data['dropoff_lon'])
        )
        
        # Request ride using user_id from token
        result = ride_service.request_ride(
            user_id=g.user_id,
            pickup=pickup,
            dropoff=dropoff
        )
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@ride_bp.route('/<int:ride_id>/status', methods=['GET'])
@jwt_handler.token_required()
def get_ride_status(ride_id):
    try:
        print(f"Fetching status for ride {ride_id}, user_id: {g.user_id}, role: {g.role}")  # Debug log
        
        result = ride_service.get_ride_status(ride_id)
        print(f"Result from ride_service: {result}")  # Debug log
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        
        if not result:
            return jsonify({"error": "Ride not found"}), 404
            
        # Check if user has access to this ride
        print(f"Checking access - User ID from token: {g.user_id}, Role: {g.role}, Ride user_id: {result.get('user_id')}")  # Debug log
        if g.role != 'admin' and g.role != 'driver':
            if int(result.get('user_id')) != int(g.user_id):  # Match the case with what RideService returns
                print(f"Access denied - User IDs don't match: {result.get('user_id')} != {g.user_id}")  # Debug log
                return jsonify({"error": "Access denied"}), 403
                
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in get_ride_status: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

@ride_bp.route('/<int:ride_id>/cancel', methods=['POST'])
@jwt_handler.token_required()
def cancel_ride(ride_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400
            
        cancellation_reason = data.get('cancellation_reason')
        cancellation_fee = data.get('cancellation_fee', 0.0)  # Default to 0 if not provided
        
        if not cancellation_reason:
            return jsonify({"error": "Cancellation reason is required"}), 400
            
        result = ride_service.cancel_ride(ride_id, cancellation_reason, cancellation_fee)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ride_bp.route('/<int:ride_id>/eta', methods=['GET'])
@jwt_handler.token_required()
def get_ride_eta(ride_id):
    try:
        result = ride_service.get_ride_eta(ride_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
