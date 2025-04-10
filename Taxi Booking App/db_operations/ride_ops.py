import sqlite3
from db.connect_db import DatabaseConnector

def save_ride(data):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
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
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()

def get_ride_status_by_id(ride_id):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT Status FROM Rides WHERE RideID = ?", (ride_id,))
    ride = cursor.fetchone()
    conn.close()
    return ride

def get_available_drivers():
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DriverID, Latitude, Longitude
        FROM Drivers
        WHERE Status = 'Available' AND Latitude IS NOT NULL AND Longitude IS NOT NULL
    """)
    drivers = cursor.fetchall()
    conn.close()
    return drivers

def get_ride_coordinates(ride_id):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT PickupLatitude, PickupLongitude, DropoffLatitude, DropoffLongitude FROM Rides WHERE RideID = ?", (ride_id,))
    ride = cursor.fetchone()
    conn.close()
    return ride

def assign_driver_to_ride(driver_id, ride_id, fare):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Rides SET Fare = ? WHERE RideID = ?", (fare, ride_id))
        cursor.execute("UPDATE Rides SET DriverID = ?, Status = 'Ongoing' WHERE RideID = ?", (driver_id, ride_id))
        cursor.execute("UPDATE Drivers SET Status = 'Busy' WHERE DriverID = ?", (driver_id,))
        conn.commit()
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()
