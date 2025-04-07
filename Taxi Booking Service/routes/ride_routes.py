import sqlite3
from flask import Blueprint, request, jsonify
from connect_db import get_db_connection
import math

ride_bp = Blueprint("ride", __name__)

#  Haversine formula to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    Radius  = 6371  # Radius of Earth in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    Compute_central_angle = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return Radius  * Compute_central_angle  

@ride_bp.route("/book", methods=["POST"])
def book_ride():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["user_id", "pickup_latitude", "pickup_longitude", "pickup_location",
                       "dropoff_latitude", "dropoff_longitude", "dropoff_location"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        user_id = int(data["user_id"])
        pickup_latitude = float(data["pickup_latitude"])
        pickup_longitude = float(data["pickup_longitude"])
        pickup_location = data["pickup_location"]
        dropoff_latitude = float(data["dropoff_latitude"])
        dropoff_longitude = float(data["dropoff_longitude"])
        dropoff_location = data["dropoff_location"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT UserID FROM Users WHERE UserID = ?", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User ID does not exist"}), 400

        cursor.execute("""
            SELECT DriverID, Latitude, Longitude
            FROM Drivers
            WHERE Status = 'Available' AND Latitude IS NOT NULL AND Longitude IS NOT NULL
        """)
        available_drivers = cursor.fetchall()

        if not available_drivers:
            return jsonify({"error": "No available drivers nearby!"}), 400

        nearest_driver = min(
            available_drivers,
            key=lambda driver: calculate_distance(pickup_latitude, pickup_longitude, float(driver[1]), float(driver[2]))
            )

        assigned_driver_id = int(nearest_driver[0])
        
        distance_km = calculate_distance(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude)
        per_km_rate = 10.0
        base_fare = 20.0

        distance_fare = distance_km * per_km_rate
        estimated_fare = round(base_fare + distance_fare, 2)
        
        cursor.execute("""
            INSERT INTO Rides (UserID, DriverID, Pickup_Location, Dropoff_Location, PickupLatitude, PickupLongitude, 
                              DropoffLatitude, DropoffLongitude, Status, Fare)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
        """, (user_id, assigned_driver_id, pickup_location, dropoff_location, pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude, estimated_fare))

        ride_id = cursor.lastrowid

        cursor.execute("UPDATE Drivers SET Status = 'Busy' WHERE DriverID = ?", (assigned_driver_id,))

        conn.commit()
        return jsonify({
            "message": "Ride booked successfully!",
            "ride_id": ride_id,
            "ride_status": "Pending",
            "driver_id": assigned_driver_id,
            "estimated_fare": estimated_fare
        }), 201

    except (ValueError, TypeError) as e:
        return jsonify({"error": "Invalid data format"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

@ride_bp.route("/accept", methods=["POST"])
def accept_ride():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["ride_id", "driver_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        ride_id = int(data["ride_id"])
        driver_id = int(data["driver_id"])

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT Status, DriverID FROM Rides WHERE RideID = ?", (ride_id,))
        ride = cursor.fetchone()

        if not ride:
            return jsonify({"error": "Ride not found"}), 404
        if ride[0] != "Pending":
            return jsonify({"error": "Ride is not available for acceptance"}), 400
        if int(ride[1]) != driver_id:
            return jsonify({"error": "This ride is assigned to another driver"}), 403

        #  Update ride and driver status
        cursor.execute("UPDATE Rides SET Status = 'Accepted' WHERE RideID = ?", (ride_id,))
        cursor.execute("UPDATE Drivers SET Status = 'On Ride' WHERE DriverID = ?", (driver_id,))

        conn.commit()
        return jsonify({
            "message": "Ride accepted successfully!",
            "ride_id": ride_id,
            "ride_status": "Accepted",
            "driver_id": driver_id
        }), 200

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data format"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()
