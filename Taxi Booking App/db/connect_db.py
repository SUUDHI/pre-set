import sqlite3

class DatabaseConnector:
    DB_PATH = "taxi_booking.db"  # Ensure this path exists and is correct

    @classmethod
    def get_connection(cls):
        return sqlite3.connect(cls.DB_PATH)
