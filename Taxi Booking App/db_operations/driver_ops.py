import sqlite3
from db.connect_db import DatabaseConnector

def save_driver(data):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Drivers (
                Driver_name, Driver_phone, Driver_email, Password,
                Driver_birth, Driver_licensePlate, Driver_gender
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["phone"],
                data["email"],
                data["password"],
                data["birth"],
                data["license_plate"],
                data["gender"]
            )
        )
        conn.commit()
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()

def get_driver_by_credentials(email, password):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Drivers WHERE Driver_email = ? AND Password = ?",
        (email, password)
    )
    driver = cursor.fetchone()
    conn.close()
    return driver

def mark_driver_available(driver_id):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Drivers SET Status = 'Available' WHERE DriverID = ?", (driver_id,))
    conn.commit()
    conn.close()
