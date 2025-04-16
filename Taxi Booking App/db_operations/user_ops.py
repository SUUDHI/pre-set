import sqlite3
from db.connect_db import DatabaseConnector
from datetime import datetime

def save_user(data):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        # Get role ID
        cursor.execute("SELECT RoleID FROM Role WHERE Name = ?", (data["role"],))
        role = cursor.fetchone()
        if not role:
            raise ValueError(f"Invalid role: {data['role']}")
        
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
        
        # If user is a driver, insert driver details
        if data["role"] == "driver" and "licensePlate" in data:
            user_id = cursor.lastrowid
            cursor.execute(
                """
                INSERT INTO Driver (
                    UserID, LicensePlate
                ) VALUES (?, ?)
                """,
                (
                    user_id,
                    data["licensePlate"]
                )
            )
        
        conn.commit()
        return {"success": True, "message": "User registered successfully"}
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_user_by_email(email):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, r.Name as Role 
            FROM Users u
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE u.Email = ?
            """,
            (email,)
        )
        user = cursor.fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

def get_user_by_phone(phone):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, r.Name as Role 
            FROM Users u
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE u.Phone = ?
            """,
            (phone,)
        )
        user = cursor.fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*, r.Name as Role 
            FROM Users u
            JOIN Role r ON u.RoleID = r.RoleID
            WHERE u.UserID = ?
            """,
            (user_id,)
        )
        user = cursor.fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

def get_driver_details(user_id):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT d.*, ds.Name as Status
            FROM Driver d
            LEFT JOIN DriverStatus ds ON d.StatusID = ds.StatusID
            WHERE d.UserID = ?
            """,
            (user_id,)
        )
        driver = cursor.fetchone()
        return dict(driver) if driver else None
    finally:
        conn.close()
