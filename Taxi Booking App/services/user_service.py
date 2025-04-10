from utils.jwt_handler import generate_token
from db_operations.user_ops import save_user, get_user_by_credentials
import sqlite3

class UserService:
    def register_user(self, data):
        try:
            save_user(data)
            return {"message": "User registered successfully!"}, 201
        except sqlite3.IntegrityError as e:
            return {"error": f"Integrity error: {str(e)}"}, 400
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def login_user(self, email, password):
        user = get_user_by_credentials(email, password)

        if user:
            token = generate_token({"user_id": user["UserID"], "role": "user"})
            return {"token": token}, 200
        else:
            return {"error": "Invalid credentials"}, 401
