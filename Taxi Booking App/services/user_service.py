from db.connect_db import DatabaseConnector
from utils.jwt_handler import generate_token
import sqlite3


class UserService:
    def register_user(self, data):
        conn = None
        
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
                
    def login_user(self, email, password):
            conn = DatabaseConnector.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Users WHERE Email = ? AND Password = ?", (email, password))
            user = cursor.fetchone()

            if user:
                token = generate_token({"user_id": user["UserID"], "role": "user"})
                return {"token": token}, 200
            else:
                return {"error": "Invalid credentials"}, 401
