from flask import Blueprint, request, jsonify, g
from services.ride_service import RideService
from utils.coordinate import Coordinate
from utils.jwt_utils import token_required
from utils.validators import validate_ride_data

ride_bp = Blueprint('ride', __name__)
ride_service = RideService()

@ride_bp.route('/request', methods=['POST'])
@token_required()
def request_ride():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400
            
        # Validate ride data
        is_valid, error_message = validate_ride_data(data)
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
@token_required()
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
@token_required()
def cancel_ride(ride_id):
    try:
        result = ride_service.cancel_ride(ride_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ride_bp.route('/<int:ride_id>/eta', methods=['GET'])
@token_required()
def get_ride_eta(ride_id):
    try:
        result = ride_service.get_ride_eta(ride_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
