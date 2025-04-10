import sqlite3
from db.connect_db import DatabaseConnector

def save_user(data):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (Name, Phone, Email, Password) VALUES (?, ?, ?, ?)",
            (data["name"], data["phone"], data["email"], data["password"])
        )
        conn.commit()
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()

def get_user_by_credentials(email, password):
    conn = DatabaseConnector.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE Email = ? AND Password = ?",
        (email, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user
