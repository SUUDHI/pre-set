import sqlite3
from db.connect_db import DatabaseConnector
from datetime import datetime
from utils.distance_utils import calculate_distance, calculate_eta


def create_ride(ride_data: dict) -> int:
    """
    Create a new ride record in the database.
    
    Args:
        ride_data (dict): Ride details including user_id, pickup/dropoff coordinates, fare, etc.
        
    Returns:
        int: ID of the created ride
    """
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        # Get status ID for 'requested'
        cursor.execute("SELECT StatusID FROM RideStatus WHERE Name = ?", ("requested",))
        status = cursor.fetchone()
        if not status:
            raise ValueError("Requested status not found")
        
        status_id = status[0]
        
        # Insert ride record
        cursor.execute(
            """
            INSERT INTO Rides (
                UserID, PickupLat, PickupLon, DropoffLat, DropoffLon,
                Fare, StatusID, CreatedAt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ride_data["user_id"],
                ride_data["pickup_lat"],
                ride_data["pickup_lon"],
                ride_data["dropoff_lat"],
                ride_data["dropoff_lon"],
                ride_data["fare"],
                status_id,
                ride_data["created_at"]
            )
        )
        
        ride_id = cursor.lastrowid
        conn.commit()
        return ride_id
        
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_ride_by_id(ride_id: int) -> dict:
    """
    Get detailed ride information by ID.
    
    Args:
        ride_id (int): ID of the ride
        
    Returns:
        dict: Ride details or None if not found
    """
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        print(f"Database: Fetching ride {ride_id}")  # Debug log
        
        cursor.execute(
            """
            SELECT 
                r.RideID,
                r.UserID,
                r.DriverID,
                r.StatusID,
                r.Fare,
                r.CancellationFee,
                r.CancellationReason,
                r.RequestedAt,
                r.PickupTime,
                r.DropoffTime,
                r.PickupLat,
                r.PickupLon,
                r.DropoffLat,
                r.DropoffLon,
                rs.Name as Status,
                u.Name as UserName,
                d_user.Name as DriverName,
                d.LicensePlate
            FROM Rides r
            LEFT JOIN RideStatus rs ON r.StatusID = rs.StatusID
            LEFT JOIN Users u ON r.UserID = u.UserID
            LEFT JOIN Users d_user ON r.DriverID = d_user.UserID
            LEFT JOIN Driver d ON r.DriverID = d.UserID
            WHERE r.RideID = ?
            """,
            (ride_id,)
        )
        ride = cursor.fetchone()
        
        if ride:
            print(f"Database: Found ride: {dict(ride)}")  # Debug log
            return dict(ride)
        else:
            print(f"Database: No ride found with ID {ride_id}")  # Debug log
            return None
            
    except sqlite3.Error as e:
        print(f"Database: Error fetching ride: {str(e)}")  # Debug log
        raise e
    finally:
        conn.close()


def update_ride_status(ride_id: int, status_name: str) -> None:
    """
    Update the status of a ride.
    
    Args:
        ride_id (int): ID of the ride
        status_name (str): New status name
    """
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        # Get status ID
        cursor.execute("SELECT StatusID FROM RideStatus WHERE Name = ?", (status_name,))
        status = cursor.fetchone()
        if not status:
            raise ValueError(f"Invalid status: {status_name}")
        
        status_id = status[0]
        
        # Update ride status
        cursor.execute(
            """
            UPDATE Rides 
            SET StatusID = ?
            WHERE RideID = ?
            """,
            (status_id, ride_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_active_rides() -> list:
    """
    Get all active rides (not completed or cancelled).
    
    Returns:
        list: List of active rides
    """
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT r.*, rs.Name as Status
            FROM Rides r
            JOIN RideStatus rs ON r.StatusID = rs.StatusID
            WHERE rs.Name NOT IN ('completed', 'cancelled')
            """
        )
        rides = cursor.fetchall()
        return [dict(ride) for ride in rides]
    finally:
        conn.close()


def assign_driver_to_ride(ride_id: int, driver_id: int) -> None:
    """
    Assign a driver to a ride.
    
    Args:
        ride_id (int): ID of the ride
        driver_id (int): ID of the driver
    """
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Rides 
            SET DriverID = ?
            WHERE RideID = ?
            """,
            (driver_id, ride_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def save_ride(data):
    """
    Save a new ride to the database.
    
    Args:
        data (dict): Ride data containing user_id, coordinates, and other details
        
    Returns:
        int: ID of the created ride
    """
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        # Get status ID for 'requested'
        cursor.execute("SELECT StatusID FROM RideStatus WHERE Name = ?", ("requested",))
        status = cursor.fetchone()
        if not status:
            raise ValueError("Requested status not found")
        
        status_id = status[0]
        
        cursor.execute(
            """INSERT INTO Rides (
                UserID, DriverID, StatusID, 
                Fare, PickupLat, PickupLon,
                DropoffLat, DropoffLon, RequestedAt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data["user_id"],
                None,  # DriverID starts as NULL
                status_id,
                data["fare"],
                data["pickup_lat"],
                data["pickup_lon"],
                data["dropoff_lat"],
                data["dropoff_lon"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_pickup_time(ride_id: int) -> None:
    """Update the pickup time for a ride when driver starts the trip."""
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Rides 
            SET PickupTime = ?, StatusID = (SELECT StatusID FROM RideStatus WHERE Name = 'in_progress')
            WHERE RideID = ?""",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ride_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_dropoff_time(ride_id: int) -> None:
    """Update the dropoff time for a ride when driver completes the trip."""
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Rides 
            SET DropoffTime = ?, StatusID = (SELECT StatusID FROM RideStatus WHERE Name = 'completed')
            WHERE RideID = ?""",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ride_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_ride_status_by_id(ride_id):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT StatusID FROM Rides WHERE RideID = ?", (ride_id,))
    ride = cursor.fetchone()
    conn.close()
    return ride


def get_available_drivers():
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.DriverID, d.Latitude, d.Longitude
        FROM Driver d
        JOIN DriverStatus ds ON d.StatusID = ds.StatusID
        WHERE ds.StatusName = 'available' 
        AND d.Latitude IS NOT NULL 
        AND d.Longitude IS NOT NULL
    """)
    drivers = cursor.fetchall()
    conn.close()
    return drivers


def get_ride_coordinates(ride_id):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PickupLat, PickupLon, DropoffLat, DropoffLon,
               PickupTime, DropoffTime
        FROM Rides 
        WHERE RideID = ?
    """, (ride_id,))
    ride = cursor.fetchone()
    conn.close()
    return ride


def get_fare_by_ride_id(ride_id):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT Fare FROM Rides WHERE RideID = ?", (ride_id,))
    ride = cursor.fetchone()
    conn.close()
    return ride


def update_ride_as_cancelled(ride_id, reason, cancellation_fee):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Rides
        SET StatusID = (SELECT StatusID FROM RideStatus WHERE StatusName = 'cancelled'),
            CancellationReason = ?,
            Fare = ?
        WHERE RideID = ?
    """, (reason, cancellation_fee, ride_id))
    conn.commit()
    conn.close()


def calculate_ride_eta(ride_id: int) -> dict:
    """
    Calculate ETA for a ride based on driver's current location and pickup location.
    Returns dictionary with distance and ETA information.
    """
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get ride and driver information
        cursor.execute("""
            SELECT r.PickupLat, r.PickupLon, d.Latitude, d.Longitude
            FROM Rides r
            JOIN Driver d ON r.DriverID = d.UserID
            WHERE r.RideID = ?
        """, (ride_id,))
        result = cursor.fetchone()
        
        if not result:
            raise ValueError("Ride not found or no driver assigned")
        
        # Calculate distance
        distance = calculate_distance(
            result['Latitude'], result['Longitude'],
            result['PickupLat'], result['PickupLon']
        )
        
        # Calculate ETA in minutes
        eta_minutes = calculate_eta(distance)
        
        # Convert to hours and format
        eta_hours = eta_minutes / 60
        eta_formatted = f"{int(eta_minutes // 60)}h {int(eta_minutes % 60)}m" if eta_minutes >= 60 else f"{int(eta_minutes)}m"
        
        return {
            "distance_km": round(distance, 2),
            "eta_hours": round(eta_hours, 2),
            "eta_formatted": eta_formatted
        }
        
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()


def get_ride_with_eta(ride_id: int) -> dict:
    """
    Get ride details including ETA information.
    """
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get ride details
        ride = get_ride_by_id(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        # Calculate ETA if driver is assigned
        if ride['DriverID']:
            eta_info = calculate_ride_eta(ride_id)
            ride_dict = dict(ride)
            ride_dict.update(eta_info)
            return ride_dict
        
        return dict(ride)
        
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()


def cancel_ride(ride_id: int, reason: str, cancellation_fee: float = 0.0) -> None:
    """
    Cancel a ride with reason and optional cancellation fee.
    
    Args:
        ride_id (int): ID of the ride to cancel
        reason (str): Reason for cancellation
        cancellation_fee (float): Fee charged for cancellation, defaults to 0
    """
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Rides 
            SET StatusID = (SELECT StatusID FROM RideStatus WHERE Name = 'cancelled'),
                CancellationReason = ?,
                CancellationFee = ?
            WHERE RideID = ?""",
            (reason, cancellation_fee, ride_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
