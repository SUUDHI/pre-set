from flask import Blueprint, request, jsonify
from services.ride_service import RideService
from utils.validators import validate_ride_data
from utils.jwt_utils import token_required

ride_bp = Blueprint("ride", __name__)
ride_service = RideService()


@ride_bp.route("/request", methods=["POST"])
@token_required(role="user")  
def request_ride():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["user_id", "pickup_location", "dropoff_location"]
    is_valid, message = validate_ride_data(data, required_fields)
    if not is_valid:
        return jsonify({"error": message}), 400

    response, status = ride_service.request_ride(data)
    return jsonify(response), status


@ride_bp.route("/status/<int:ride_id>", methods=["GET"])
def ride_status(ride_id):
    response, status = ride_service.get_ride_status(ride_id)
    return jsonify(response), status


@ride_bp.route("/assign-driver", methods=["POST"])
@token_required(role="driver")
def assign_driver():
    data = request.get_json()
    required = ["ride_id", "pickup_lat", "pickup_lng"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    response, status = ride_service.assign_nearest_driver(
        data["ride_id"],
        data["pickup_lat"],
        data["pickup_lng"]
    )
    return jsonify(response), status

@ride_bp.route("/cancel", methods=["POST"])
@token_required(role="user")
def cancel_ride():
    data = request.get_json()
    ride_id = data.get("ride_id")
    reason = data.get("reason")

    if not ride_id or not reason:
        return jsonify({"error": "ride_id and reason are required"}), 400

    response, status = ride_service.cancel_ride(ride_id, reason)
    return jsonify(response), status
