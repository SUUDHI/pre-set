# services/user_service.py
import sqlite3
from db.connect_db import DatabaseConnector
from utils.jwt_handler import jwt_handler

class UserService:
    def register_user(self, data):
        try:
            conn = DatabaseConnector.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Users (name, phone, email, password, birth, gender, role)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["name"],
                    data["phone"],
                    data["email"],
                    data["password"],
                    data.get("birth"),
                    data.get("gender"),
                    data["role"]
                )
            )
            conn.commit()
            return {"message": f"{data['role'].capitalize()} registered successfully."}, 201
        except sqlite3.IntegrityError as e:
            return {"error": f"Integrity error: {str(e)}"}, 400
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        finally:
            conn.close()

    def login_user(self, email, password):
        try:
            conn = DatabaseConnector.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

            if user:
                payload = {"user_id": user["id"], "role": user["role"]}
                token = jwt_handler.generate_token(payload)
                return {"token": token, "role": user["role"]}, 200
            return {"error": "Invalid credentials"}, 401

        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500
        finally:
            conn.close()


