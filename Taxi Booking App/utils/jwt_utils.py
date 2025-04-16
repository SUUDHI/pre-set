import jwt
from functools import wraps
from flask import request, jsonify, g, current_app
from utils.config import SECRET_KEY
from datetime import datetime, timedelta

def token_required(role=None):
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
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                g.user_id = data.get("user_id")
                g.role = data.get("role")

                if role and g.role != role:
                    return jsonify({"error": "Access forbidden: incorrect role"}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired!"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token!"}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator

def generate_token(payload):
    """
    Generate a JWT token with the given payload
    """
    try:
        # Add expiration time (24 hours from now)
        payload['exp'] = datetime.utcnow() + timedelta(hours=24)
        
        # Generate token
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        return token
    except Exception as e:
        raise Exception(f"Error generating token: {str(e)}")

def verify_token(token):
    """
    Verify a JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    except Exception as e:
        raise Exception(f"Error verifying token: {str(e)}")

def get_token_from_header(request):
    """
    Extract token from Authorization header
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        # Check if header is in format "Bearer <token>"
        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None
    except Exception:
        return None
