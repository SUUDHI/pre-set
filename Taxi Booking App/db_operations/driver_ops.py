import sqlite3
from db.connect_db import DatabaseConnector
from datetime import datetime


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
                UserID, LicenseNumber, LicensePlate, VehicleType, StatusID
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                data.get("licenseNumber"),  # Using get() to handle optional fields
                data["licensePlate"],       # Required field
                data.get("vehicleType"),    # Using get() to handle optional fields
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
                d.VehicleType,
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