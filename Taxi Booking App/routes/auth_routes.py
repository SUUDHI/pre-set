from flask import Blueprint, request, jsonify
from utils.validators import validate_user_data
from services.user_service import UserService
from utils.jwt_handler import generate_token

auth_bp = Blueprint("auth", __name__)
user_service = UserService()


@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["name", "email", "phone", "password"]
    is_valid, message = validate_user_data(data, required_fields)
    if not is_valid:
        return jsonify({"error": message}), 400

    response, status = user_service.register_user(data)
    return jsonify(response), status

@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    response, status = user_service.login_user(email, password)
    return jsonify(response), status
