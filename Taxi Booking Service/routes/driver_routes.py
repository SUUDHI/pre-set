import sqlite3 
from flask import Blueprint, request, jsonify, render_template
from connect_db import get_db_connection

driver_bp = Blueprint("driver", __name__)

@driver_bp.route("/register", methods=["POST"])
def register_driver():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["Driver_name", "Driver_phone", "Driver_email", "Password", "Driver_birth", "Driver_licensePlate", "Driver_gender"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA journal_mode=WAL;")  

        cursor.execute("""
            INSERT INTO Drivers (Driver_name, Driver_phone, Driver_email, Password, Driver_birth, Driver_licensePlate, Driver_gender, Status, current_location) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Available', '0,0')
        """, (data["Driver_name"], data["Driver_phone"], data["Driver_email"], data["Password"], 
              data["Driver_birth"], data["Driver_licensePlate"], data["Driver_gender"]))
        
        conn.commit()
        return jsonify({"message": "Driver registered successfully!"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Phone number, email, or license plate already exists!"}), 400

    finally:
        cursor.close() 
        conn.close() 

#http://localhost:5000/driver/login
@driver_bp.route("/driver/login", methods=["POST"])
def driver_login():
    data = request.json
    email = data.get("Driver_email")
    password = data.get("Password")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DriverID FROM Drivers WHERE Driver_email = ? AND Password = ?", (email, password))
    driver = cursor.fetchone()
    conn.close()

    if driver:
        return jsonify({"message": "Login successful", "DriverID": driver[0]}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 400

#http://127.0.0.1:5000/driver/update_status
@driver_bp.route('/driver/update_status', methods=['PATCH'])
def update_driver_status():
    data = request.get_json()
    driver_id = data.get("driver_id")

    if not driver_id:
        return jsonify({"error": "Driver ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Status FROM drivers WHERE DriverID = ?", (driver_id,))
    driver = cursor.fetchone()

    if not driver:
        conn.close()
        return jsonify({"error": "Driver not found"}), 404

    new_status = "Available" if driver["Status"] == "Busy" else "Offline"
    cursor.execute("UPDATE drivers SET Status = ? WHERE DriverID = ?", (new_status, driver_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated successfully", "new_status": new_status})

@driver_bp.route('/driver/dashboard', methods=['GET'])
def driver_dashboard():
    driver_id = request.args.get('driver_id')

    if not driver_id:
        return jsonify({"error": "Driver ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drivers WHERE DriverID = ?", (driver_id,))
    driver = cursor.fetchone()
    conn.close()

    if driver:
        return render_template("driver_dashboard.html", driver=driver)
    else:
        return jsonify({"error": "Driver not found"}), 404

#http://127.0.0.1:5000/driver/available
@driver_bp.route("/available", methods=["GET"])
def get_available_drivers():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DriverID, Driver_name, Driver_phone, Driver_licensePlate, Status FROM Drivers WHERE Status = 'Available'")
    drivers = cursor.fetchall()
    conn.close()

    return jsonify([{"DriverID": d[0], "Driver_name": d[1], "Driver_phone": d[2], "Driver_licensePlate": d[3], "Status": d[4]} for d in drivers])
