from db.connect_db import DatabaseConnector
from utils.distance import calculate_distance
from utils.fare import calculate_fare
import sqlite3


class RideService:
    def request_ride(self, data):
       
        try:
            conn = DatabaseConnector.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO Rides (
                    UserID, Pickup_Location, Dropoff_Location, 
                    PickupLatitude, PickupLongitude, DropoffLatitude, DropoffLongitude
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    data["user_id"],
                    data["pickup_location"],
                    data["dropoff_location"],
                    data.get("pickup_lat"),
                    data.get("pickup_lng"),
                    data.get("dropoff_lat"),
                    data.get("dropoff_lng")
                )
            )
            conn.commit()
            return {"message": "Ride requested successfully!"}, 201
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        finally:
            if conn:
                conn.close()

    def get_ride_status(self, ride_id):
        
        try:
            conn = DatabaseConnector.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Status FROM Rides WHERE RideID = ?", (ride_id,))
            row = cursor.fetchone()

            if row:
                return {"ride_id": ride_id, "status": row["Status"]}, 200
            else:
                return {"error": "Ride not found"}, 404
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        finally:
            if conn:
                conn.close()

    def assign_nearest_driver(self, ride_id, pickup_lat, pickup_lng):
        conn = None
        try:
            conn = DatabaseConnector.get_connection()
            conn.row_factory = sqlite3.Row  
            cursor = conn.cursor()

            cursor.execute("""
                SELECT DriverID, Latitude, Longitude
                FROM Drivers
                WHERE Status = 'Available' AND Latitude IS NOT NULL AND Longitude IS NOT NULL
            """)
            drivers = cursor.fetchall()

            if not drivers:
                return {"error": "No available drivers found"}, 404

            nearest_driver = min(
                drivers,
                key=lambda d: calculate_distance(
                    pickup_lat, pickup_lng, d["Latitude"], d["Longitude"]
                )
            )

            driver_id = nearest_driver["DriverID"]

            cursor.execute("SELECT PickupLatitude, PickupLongitude, DropoffLatitude, DropoffLongitude FROM Rides WHERE RideID = ?", (ride_id,))
            ride = cursor.fetchone()
            if not ride:
                return {"error": "Ride not found"}, 404

            if (
                ride["PickupLatitude"] is None or ride["PickupLongitude"] is None or
                ride["DropoffLatitude"] is None or ride["DropoffLongitude"] is None
            ):
                return {"error": "Ride pickup or dropoff coordinates are missing"}, 400


            fare = calculate_fare(
                ride["PickupLatitude"], ride["PickupLongitude"],
                ride["DropoffLatitude"], ride["DropoffLongitude"]
            )

            cursor.execute("UPDATE Rides SET Fare = ? WHERE RideID = ?", (fare, ride_id))

            cursor.execute("UPDATE Rides SET DriverID = ?, Status = 'Ongoing' WHERE RideID = ?", (driver_id, ride_id))
            cursor.execute("UPDATE Drivers SET Status = 'Busy' WHERE DriverID = ?", (driver_id,))
            conn.commit()

            return {
                "message": "Driver auto-assigned successfully",
                "driver_id": driver_id
            }, 200

        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

        finally:
            if conn:
                conn.close()
