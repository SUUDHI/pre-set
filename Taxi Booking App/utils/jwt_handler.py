import jwt
from functools import wraps
from flask import request, jsonify, g, current_app
from datetime import datetime, timedelta
from utils.config import SECRET_KEY

class JWTHandler:
    @staticmethod
    def generate_token(payload: dict, expiry_hours: int = 24) -> str:
        """Generate a JWT token with the given payload."""
        try:
            expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
            payload['exp'] = expiry
            return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        except Exception as e:
            raise Exception(f"Error generating token: {str(e)}")

    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and validate a JWT token."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
        except Exception as e:
            raise Exception(f"Error decoding token: {str(e)}")

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify a JWT token and return the payload if valid."""
        try:
            return JWTHandler.decode_token(token)
        except Exception as e:
            raise Exception(f"Error verifying token: {str(e)}")

    @staticmethod
    def token_required(role: str = None):
        """Decorator to protect routes with JWT authentication."""
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                token = None
                if 'Authorization' in request.headers:
                    auth_header = request.headers['Authorization']
                    if auth_header.startswith("Bearer "):
                        token = auth_header.split(" ")[1]

                if not token:
                    return jsonify({"error": "Token is missing!"}), 401

                try:
                    data = JWTHandler.decode_token(token)
                    g.user_id = data.get("user_id")
                    g.role = data.get("role")

                    if role and g.role != role:
                        return jsonify({"error": "Access forbidden: incorrect role"}), 403

                except jwt.ExpiredSignatureError:
                    return jsonify({"error": "Token has expired!"}), 401
                except jwt.InvalidTokenError:
                    return jsonify({"error": "Invalid token!"}), 401
                except Exception as e:
                    return jsonify({"error": f"Token error: {str(e)}"}), 401

                return f(*args, **kwargs)
            return wrapper
        return decorator

# Create a singleton instance
jwt_handler = JWTHandler()
