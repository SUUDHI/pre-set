from db.connect_db import DatabaseConnector
import sqlite3


class DriverService:
    def register_driver(self, data):
        """
        Registers a new driver in the system.
        """
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
