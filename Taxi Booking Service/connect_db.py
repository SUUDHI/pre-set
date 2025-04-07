import sqlite3

DATABASE_NAME = "taxi_booking.db"

def get_db_connection():
    conn = sqlite3.connect("taxi_booking.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  
    return conn
