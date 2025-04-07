from flask import Blueprint, request, jsonify
from connect_db import get_db_connection
import sqlite3

auth_bp = Blueprint("auth", __name__)

#  User Registration
@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    required_fields = ["Name", "Phone", "Email", "Password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        print(" Connected to database. Inserting user...")
        cursor.execute(
            "INSERT INTO Users (Name, Phone, Email, Password) VALUES (?, ?, ?, ?)",
            (data["Name"], data["Phone"], data["Email"], data["Password"]),
        )
        conn.commit()   
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({"error": "Phone or Email already exists!"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": "Database error occurred!"}), 500
    except Exception as e:
        return jsonify({"error": "Something went wrong!"}), 500
    
#  User Login
#http://127.0.0.1:5000/auth/login
@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["Email", "Password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT UserID FROM Users WHERE Email = ? AND Password = ?", (data["Email"], data["Password"]))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful!", "UserID": user[0]})
    else:
        return jsonify({"error": "Invalid email or password!"}), 401
