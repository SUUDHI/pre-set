from flask import Blueprint, request, jsonify, g
from services.driver_service import DriverService
from services.validators import DriverValidator
from utils.jwt_handler import jwt_handler
from db.connect_db import DatabaseConnector
from utils.auth import token_required
from db_operations.driver_ops import DriverOps
import sqlite3

driver_bp = Blueprint("driver", __name__)
driver_service = DriverService()
driver_validator = DriverValidator()
driver_ops = DriverOps()

@driver_bp.route("/register", methods=["POST"])
def register_driver():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    is_valid, message = driver_validator.validate(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    response, status = driver_service.register_driver(data)
    return jsonify(response), status

@driver_bp.route("/login", methods=["POST"])
def login_driver():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    response, status = driver_service.login_driver(email, password)
    return jsonify(response), status

@driver_bp.route("/location", methods=["POST", "PUT"])
@jwt_handler.token_required(role="driver")
def update_driver_location():
    """Update driver's current location"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and longitude are required"}), 400

        conn = DatabaseConnector.get_connection()
        cursor = conn.cursor()

        # Update driver's location in the database
        cursor.execute("""
            UPDATE Driver 
            SET Latitude = ?, Longitude = ?
            WHERE UserID = ?
        """, (latitude, longitude, g.user_id))

        conn.commit()
        return jsonify({"message": "Location updated successfully"}), 200

    except Exception as e:
        print(f"Error updating location: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@driver_bp.route("/status", methods=["GET", "POST", "PUT"])
@jwt_handler.token_required(role="driver")
def handle_driver_status():
    """Handle all driver status operations"""
    try:
        if request.method == "GET":
            status = driver_ops.get_driver_status(g.user_id)
            if status is None:
                return jsonify({'error': 'Driver not found'}), 404
            return jsonify({'status': status, 'driver_id': g.user_id})

        # POST or PUT
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({"error": "Status is required"}), 400

        status = data['status'].lower()
        valid_statuses = ['available', 'busy', 'offline']
        
        if status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400

        conn = DatabaseConnector.get_connection()
        cursor = conn.cursor()

        # Map status to StatusID
        status_map = {
            'offline': 1,
            'available': 2,
            'busy': 3
        }

        # Update driver's status
        cursor.execute("""
            UPDATE Driver 
            SET StatusID = ?
            WHERE UserID = ?
        """, (status_map[status], g.user_id))

        conn.commit()
        return jsonify({
            'message': 'Status updated successfully',
            'status': status,
            'driver_id': g.user_id
        })

    except Exception as e:
        print(f"Error handling driver status: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@driver_bp.route("/rides/<int:ride_id>/accept", methods=["POST"])
@jwt_handler.token_required(role="driver")
def accept_ride(ride_id):
    """Accept a ride request by a driver"""
    try:
        response, status = driver_service.accept_ride(g.user_id, ride_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@driver_bp.route("/rides/requested", methods=["GET"])
@jwt_handler.token_required(role="driver")
def get_requested_rides():
    """Get all available ride requests"""
    try:
        response, status = driver_service.get_requested_rides(g.user_id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@driver_bp.route("/rides/assigned", methods=["GET"])
@jwt_handler.token_required(role="driver")
def get_assigned_rides():
    """Get all rides assigned to the driver"""
    try:
        conn = DatabaseConnector.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                r.RideID,
                r.UserID,
                r.PickupLat,
                r.PickupLon,
                r.DropoffLat,
                r.DropoffLon,
                r.Fare,
                r.RequestedAt,
                r.PickupTime,
                rs.Name as Status,
                u.Name as UserName,
                u.Phone as UserPhone
            FROM Rides r
            JOIN Users u ON r.UserID = u.UserID
            JOIN RideStatus rs ON r.StatusID = rs.StatusID
            WHERE r.DriverID = ?
            AND rs.Name IN ('accepted', 'in_progress')
            ORDER BY r.RequestedAt DESC
        """, (g.user_id,))
        
        rides = cursor.fetchall()
        return jsonify([dict(ride) for ride in rides]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@driver_bp.route("/vehicle-types", methods=["GET"])
def get_vehicle_types():
    """Get all available vehicle types"""
    try:
        conn = DatabaseConnector.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                VehicleTypeID,
                Name,
                Description,
                BaseRate,
                PricePerKm,
                MaxPassengers
            FROM VehicleTypes
            ORDER BY BaseRate ASC
        """)
        
        vehicle_types = []
        for row in cursor.fetchall():
            vehicle_types.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'baseRate': row[3],
                'pricePerKm': row[4],
                'maxPassengers': row[5]
            })
            
        return jsonify(vehicle_types), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@driver_bp.route("/rides/<int:ride_id>/complete", methods=["POST"])
@jwt_handler.token_required(role="driver")
def complete_ride(ride_id):
    """Complete a ride by updating its status and driver's location"""
    try:
        # Get the driver's current location from request
        data = request.get_json()
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({"error": "Current location (latitude, longitude) is required"}), 400

        response, status = driver_service.complete_ride(
            driver_id=g.user_id,
            ride_id=ride_id,
            dropoff_lat=data['latitude'],
            dropoff_lon=data['longitude']
        )
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@driver_bp.route("/rides/<int:ride_id>/start", methods=["POST"])
@jwt_handler.token_required(role="driver")
def start_ride(ride_id):
    """Start a ride by changing its status to in_progress"""
    try:
        conn = DatabaseConnector.get_connection()
        cursor = conn.cursor()
        
        # Verify the ride exists and belongs to this driver
        cursor.execute("""
            SELECT r.RideID, r.StatusID, rs.Name as Status
            FROM Rides r
            JOIN RideStatus rs ON r.StatusID = rs.StatusID
            WHERE r.RideID = ? AND r.DriverID = ?
        """, (ride_id, g.user_id))
        
        ride = cursor.fetchone()
        if not ride:
            return jsonify({"error": "Ride not found or not assigned to you"}), 404
            
        if ride[2] != 'accepted':
            return jsonify({"error": "Only accepted rides can be started"}), 400
            
        # Update ride status to in_progress
        cursor.execute("""
            UPDATE Rides 
            SET StatusID = (SELECT StatusID FROM RideStatus WHERE Name = 'in_progress'),
                PickupTime = CURRENT_TIMESTAMP
            WHERE RideID = ?
        """, (ride_id,))
        
        conn.commit()
        return jsonify({"message": "Ride started successfully"}), 200
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@driver_bp.route("/rides/<int:ride_id>/cancel", methods=["POST"])
@jwt_handler.token_required(role="driver")
def cancel_ride(ride_id):
    """Cancel a ride by driver"""
    try:
        conn = DatabaseConnector.get_connection()
        cursor = conn.cursor()
        
        # Verify the ride exists and belongs to this driver
        cursor.execute("""
            SELECT r.RideID, r.StatusID, rs.Name as Status
            FROM Rides r
            JOIN RideStatus rs ON r.StatusID = rs.StatusID
            WHERE r.RideID = ? AND r.DriverID = ?
        """, (ride_id, g.user_id))
        
        ride = cursor.fetchone()
        if not ride:
            return jsonify({"error": "Ride not found or not assigned to you"}), 404
            
        if ride[2] not in ['accepted', 'in_progress']:
            return jsonify({"error": "Only accepted or in-progress rides can be cancelled"}), 400
            
        # Update ride status to cancelled
        cursor.execute("""
            UPDATE Rides 
            SET StatusID = (SELECT StatusID FROM RideStatus WHERE Name = 'cancelled'),
                CancellationReason = ?
            WHERE RideID = ?
        """, ('Cancelled by driver', ride_id))
        
        # Update driver status to available
        cursor.execute("""
            UPDATE Driver 
            SET StatusID = (SELECT StatusID FROM DriverStatus WHERE Name = 'available')
            WHERE UserID = ?
        """, (g.user_id,))
        
        conn.commit()
        return jsonify({"message": "Ride cancelled successfully"}), 200
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()