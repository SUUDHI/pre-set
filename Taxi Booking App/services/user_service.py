from db.connect_db import DatabaseConnector
import sqlite3


class UserService:
    def register_user(self, data):
        conn = None
        """
        Registers a new user in the system.
        """
        try:
            conn = DatabaseConnector.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (Name, Phone, Email, Password) VALUES (?, ?, ?, ?)",
                (data["name"], data["phone"], data["email"], data["password"])
            )
            conn.commit()
            return {"message": "User registered successfully!"}, 201
        except sqlite3.IntegrityError as e:
            return {"error": f"Integrity error: {str(e)}"}, 400
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        finally:
            if conn:
                conn.close()
