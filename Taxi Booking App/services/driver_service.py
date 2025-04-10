from db.connect_db import DatabaseConnector
from utils.jwt_handler import generate_token
import sqlite3


class DriverService:
    def register_driver(self, data):
        
        try:
            conn = DatabaseConnector.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Drivers (Driver_name, Driver_phone, Driver_email, Password, Driver_birth, Driver_licensePlate, Driver_gender) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
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
            return {"message": "Driver registered successfully!"}, 201
        except sqlite3.IntegrityError as e:
            return {"error": f"Integrity error: {str(e)}"}, 400
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        finally:
            if conn:
                conn.close()

    def login_driver(self, email, password):
            conn = DatabaseConnector.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Drivers WHERE Driver_email = ? AND Password = ?", (email, password))
            driver = cursor.fetchone()

            if driver:
                token = generate_token({"driver_id": driver["DriverID"], "role": "driver"})
                return {"token": token}, 200
            else:
                return {"error": "Invalid credentials"}, 401

