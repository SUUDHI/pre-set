from flask import Blueprint, request, jsonify
from services.driver_service import DriverService
from utils.validators import validate_driver_data

driver_bp = Blueprint("driver", __name__)
driver_service = DriverService()


@driver_bp.route("/register", methods=["POST"])
def register_driver():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["name", "phone", "email", "password", "birth", "license_plate", "gender"]
    is_valid, message = validate_driver_data(data, required_fields)
    if not is_valid:
        return jsonify({"error": message}), 400

    response, status = driver_service.register_driver(data)
    return jsonify(response), status
