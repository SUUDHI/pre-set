from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db_operations.ride_ops import create_ride

rides_bp = Blueprint('rides', __name__)

@rides_bp.route('/request', methods=['POST'])
@jwt_required()
def request_ride():
    """
    Request a new ride
    Required fields:
    - pickup_lat: float
    - pickup_lon: float
    - dropoff_lat: float
    - dropoff_lon: float
    - vehicle_type_id: int
    """
    try:
        data = request.get_json()
        required_fields = ['pickup_lat', 'pickup_lon', 'dropoff_lat', 'dropoff_lon', 'vehicle_type_id']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Validate coordinates
        for coord in ['pickup_lat', 'pickup_lon', 'dropoff_lat', 'dropoff_lon']:
            if not isinstance(data[coord], (int, float)):
                return jsonify({'error': f'{coord} must be a number'}), 400

        # Validate vehicle type
        if not isinstance(data['vehicle_type_id'], int) or data['vehicle_type_id'] < 1:
            return jsonify({'error': 'vehicle_type_id must be a positive integer'}), 400

        # Create ride request
        ride_data = {
            'pickup_lat': float(data['pickup_lat']),
            'pickup_lon': float(data['pickup_lon']),
            'dropoff_lat': float(data['dropoff_lat']),
            'dropoff_lon': float(data['dropoff_lon']),
            'vehicle_type_id': int(data['vehicle_type_id']),
            'user_id': get_jwt_identity(),
            'status': 'PENDING'
        }

        ride_id = create_ride(ride_data)
        return jsonify({
            'message': 'Ride request created successfully',
            'ride_id': ride_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    