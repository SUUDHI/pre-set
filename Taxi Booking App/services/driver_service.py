from utils.jwt_handler import generate_token
from db_operations.driver_ops import save_driver, get_driver_by_credentials
import sqlite3

class DriverService:
    def register_driver(self, data):
        try:
            save_driver(data)
            return {"message": "Driver registered successfully!"}, 201
        except sqlite3.IntegrityError as e:
            return {"error": f"Integrity error: {str(e)}"}, 400
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}, 500

    def login_driver(self, email, password):
        driver = get_driver_by_credentials(email, password)

        if driver:
            token = generate_token({"driver_id": driver["DriverID"], "role": "driver"})
            return {"token": token}, 200
        else:
            return {"error": "Invalid credentials"}, 401