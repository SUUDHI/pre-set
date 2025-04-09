import sqlite3

class DatabaseConnector:
    DB_PATH = "taxi_booking.db" 

    @classmethod
    def get_connection(cls):
        return sqlite3.connect(cls.DB_PATH)
