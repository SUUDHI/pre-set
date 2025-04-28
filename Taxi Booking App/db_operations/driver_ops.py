import sqlite3
from db.connect_db import DatabaseConnector
from datetime import datetime
from typing import List, Dict, Any


def save_driver(data):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        # Get role ID
        cursor.execute("SELECT RoleID FROM Role WHERE Name = ?", ("driver",))
        role = cursor.fetchone()
        if not role:
            raise ValueError("Driver role not found")
        
        role_id = role[0]
        
        # Insert user
        cursor.execute(
            """
            INSERT INTO Users (
                Name, Email, Phone, Password, RoleID, Birth, Gender, CreatedAt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["email"],
                data["phone"],
                data["password"],
                role_id,
                data["birth"],
                data["gender"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        
        # Get the inserted user ID
        user_id = cursor.lastrowid
        
        # Insert driver details with all fields
        cursor.execute(
            """
            INSERT INTO Driver (
                UserID, LicenseNumber, LicensePlate, VehicleTypeID, StatusID
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                data.get("licenseNumber"),  # Using get() to handle optional fields
                data["licensePlate"],       # Required field
                data["vehicleTypeId"],      # Required field
                1  # Default status (offline)
            )
        )
        
        conn.commit()
        return {"success": True, "message": "Driver registered successfully"}
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_driver_by_email(email):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, d.*, r.Name as Role 
            FROM Users u
            JOIN Driver d ON u.UserID = d.UserID
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE u.Email = ?
            """,
            (email,)
        )
        driver = cursor.fetchone()
        return dict(driver) if driver else None
    finally:
        conn.close()


def get_driver_by_phone(phone):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, d.*, r.Name as Role 
            FROM Users u
            JOIN Driver d ON u.UserID = d.UserID
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE u.Phone = ?
            """,
            (phone,)
        )
        driver = cursor.fetchone()
        return dict(driver) if driver else None
    finally:
        conn.close()


def get_driver_by_license_plate(license_plate):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, d.*, r.Name as Role 
            FROM Users u
            JOIN Driver d ON u.UserID = d.UserID
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE d.LicensePlate = ?
            """,
            (license_plate,)
        )
        driver = cursor.fetchone()
        return dict(driver) if driver else None
    finally:
        conn.close()


def get_driver_by_credentials(email, password):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, d.*, r.Name as Role 
            FROM Users u
            JOIN Driver d ON u.UserID = d.UserID
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE u.Email = ?
            """,
            (email,)
        )
        driver = cursor.fetchone()
        return dict(driver) if driver else None
    finally:
        conn.close()


def update_driver_location(driver_id, latitude, longitude):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Driver 
            SET Latitude = ?, Longitude = ?
            WHERE UserID = ?
            """,
            (latitude, longitude, driver_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_driver_status(driver_id, status_name):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        # Get status ID
        cursor.execute("SELECT StatusID FROM DriverStatus WHERE Name = ?", (status_name,))
        status = cursor.fetchone()
        if not status:
            raise ValueError(f"Invalid status: {status_name}")
        
        status_id = status[0]
        
        # Update driver status
        cursor.execute(
            """
            UPDATE Driver 
            SET StatusID = ?
            WHERE UserID = ?
            """,
            (status_id, driver_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_available_drivers():
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, d.*, r.Name as Role, ds.Name as Status
            FROM Users u
            JOIN Driver d ON u.UserID = d.UserID
            JOIN Role r ON u.RoleID = r.RoleID
            JOIN DriverStatus ds ON d.StatusID = ds.StatusID
            WHERE ds.Name = 'available'
            """
        )
        drivers = cursor.fetchall()
        return [dict(driver) for driver in drivers]
    finally:
        conn.close()


def get_driver_by_id(driver_id: int) -> dict:
    """
    Get driver information by ID.
    
    Args:
        driver_id (int): ID of the driver
        
    Returns:
        dict: Driver information including status
    """
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                d.UserID,
                d.LicenseNumber,
                d.LicensePlate,
                d.VehicleTypeID,
                d.Latitude,
                d.Longitude,
                ds.Name as StatusName,
                u.Name,
                u.Email,
                u.Phone
            FROM Driver d
            JOIN Users u ON d.UserID = u.UserID
            JOIN DriverStatus ds ON d.StatusID = ds.StatusID
            WHERE d.UserID = ?
            """,
            (driver_id,)
        )
        driver = cursor.fetchone()
        return dict(driver) if driver else None
    finally:
        conn.close()


def get_ride_requests(driver_id: int) -> list:
    """
    Get all ride requests for a specific driver.
    
    Args:
        driver_id (int): ID of the driver
        
    Returns:
        list: List of ride requests
    """
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
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
                rs.Name as Status,
                u.Name as UserName,
                u.Phone as UserPhone
            FROM Rides r
            JOIN Users u ON r.UserID = u.UserID
            JOIN RideStatus rs ON r.StatusID = rs.StatusID
            WHERE (r.DriverID = ? OR r.DriverID IS NULL)
            AND rs.Name = 'requested'
            ORDER BY r.RequestedAt DESC
        """, (driver_id,))
        rides = cursor.fetchall()
        return [dict(ride) for ride in rides]
    except sqlite3.Error as e:
        print(f"Error fetching ride requests: {str(e)}")
        return []
    finally:
        conn.close()


def get_ride_requests_by_vehicle_type(driver_id: int, vehicle_type_id: int) -> List[Dict[str, Any]]:
    """Get all ride requests that match the driver's vehicle type"""
    conn = DatabaseConnector.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                r.RideID,
                r.UserID,
                r.VehicleTypeID,
                r.Fare,
                r.RequestedAt,
                r.PickupLat,
                r.PickupLon,
                r.DropoffLat,
                r.DropoffLon,
                rs.Name as Status,
                vt.Name as VehicleType,
                u.Name as UserName
            FROM Rides r
            JOIN RideStatus rs ON r.StatusID = rs.StatusID
            JOIN VehicleTypes vt ON r.VehicleTypeID = vt.VehicleTypeID
            JOIN Users u ON r.UserID = u.UserID
            WHERE r.StatusID = (SELECT StatusID FROM RideStatus WHERE Name = 'requested')
            AND r.VehicleTypeID = ?
            AND r.DriverID IS NULL
            ORDER BY r.RequestedAt DESC
        """, (vehicle_type_id,))
        
        rides = []
        for row in cursor.fetchall():
            rides.append({
                'RideID': row[0],
                'UserID': row[1],
                'VehicleTypeID': row[2],
                'Fare': row[3],
                'RequestedAt': row[4],
                'PickupLat': row[5],
                'PickupLon': row[6],
                'DropoffLat': row[7],
                'DropoffLon': row[8],
                'Status': row[9],
                'VehicleType': row[10],
                'UserName': row[11]
            })
        return rides
    except Exception as e:
        print(f"Error getting ride requests: {e}")
        raise e
    finally:
        conn.close()


class DriverOps:
    def __init__(self):
        pass

    def get_driver_status(self, driver_id):
        conn = None
        try:
            conn = DatabaseConnector.get_connection()
            cursor = conn.cursor()
            query = """
                SELECT ds.Name as status
                FROM Driver d
                JOIN DriverStatus ds ON d.StatusID = ds.StatusID
                WHERE d.UserID = ?
            """
            cursor.execute(query, (driver_id,))
            result = cursor.fetchone()
            return result['status'] if result else None
        except Exception as e:
            print(f"Error getting driver status: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    def update_driver_status(self, driver_id, new_status):
        conn = None
        try:
            conn = DatabaseConnector.get_connection()
            cursor = conn.cursor()
            
            # Convert status to lowercase for case-insensitive matching
            new_status_lower = new_status.lower()
            
            # First get the StatusID for the new status
            status_query = "SELECT StatusID FROM DriverStatus WHERE LOWER(Name) = ?"
            cursor.execute(status_query, (new_status_lower,))
            status_result = cursor.fetchone()
            
            if not status_result:
                raise ValueError(f"Invalid status: {new_status}. Valid statuses are: offline, available, busy")
            
            status_id = status_result['StatusID']
            
            # Update the driver's status
            update_query = "UPDATE Driver SET StatusID = ? WHERE UserID = ?"
            cursor.execute(update_query, (status_id, driver_id))
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error updating driver status: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()