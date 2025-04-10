import jwt
from functools import wraps
from flask import request, jsonify, g
import datetime
from utils.config import SECRET_KEY

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
                print("📦 Received Token:", token)
                print("🔐 Using SECRET_KEY:", SECRET_KEY)

                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                g.user_id = data.get('user_id')  
                g.driver_id = data.get('driver_id')
                g.role = data.get('role')

                if role and data.get('role') != role:
                    return jsonify({"error": "Access forbidden: incorrect role"}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired!"}), 401
            except jwt.InvalidTokenError as e:
                print("🔴 InvalidTokenError:", str(e))
                return jsonify({"error": "Invalid token!"}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator
