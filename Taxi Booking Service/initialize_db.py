import sqlite3
from connect_db import get_db_connection

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Phone TEXT UNIQUE NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Drivers (
            DriverID INTEGER PRIMARY KEY AUTOINCREMENT,
            Driver_name TEXT NOT NULL,
            Driver_phone TEXT UNIQUE NOT NULL,
            Driver_email TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            Driver_birth DATE,
            Driver_licensePlate TEXT UNIQUE NOT NULL,
            Driver_gender TEXT NOT NULL,
            Status TEXT DEFAULT 'Available',
            Current_Location TEXT DEFAULT '0,0', 
            Latitude REAL,
            Longitude REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rides (
            RideID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            DriverID INTEGER,
            Pickup_Location TEXT NOT NULL,
            Dropoff_Location TEXT NOT NULL,
            Status TEXT DEFAULT 'Pending',  
            Fare REAL DEFAULT 0.0,
            Cancellation_Reason TEXT,
            Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PickupLatitude REAL,
            PickupLongitude REAL,
            DropoffLatitude REAL,
            DropoffLongitude REAL,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            RideID INTEGER NOT NULL,
            UserID INTEGER NOT NULL,
            Amount REAL NOT NULL,
            Type TEXT NOT NULL,  
            Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (RideID) REFERENCES Rides(RideID),
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
    ''')

    conn.commit()
    conn.close()
    print(" Database initialized successfully!")

if __name__ == "__main__":
    create_tables()
