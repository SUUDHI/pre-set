from connect_db import DatabaseConnector
import sqlite3
import os

def initialize_database():
    # Delete the existing database file if it exists
    db_path = "instance/Taxi_database"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database removed.")

    # Create the instance directory if it doesn't exist
    os.makedirs("instance", exist_ok=True)

    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    
    try:
        # Drop existing tables if they exist
        cursor.executescript("""
            DROP TABLE IF EXISTS Rides;
            DROP TABLE IF EXISTS Driver;
            DROP TABLE IF EXISTS Users;
            DROP TABLE IF EXISTS RideStatus;
            DROP TABLE IF EXISTS DriverStatus;
            DROP TABLE IF EXISTS Role;
        """)
        
        # Create tables
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Role (
                RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Email TEXT UNIQUE NOT NULL,
                Phone TEXT UNIQUE NOT NULL,
                Password TEXT NOT NULL,
                Birth DATE,
                Gender TEXT,
                RoleID INTEGER,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
            );
            
            CREATE TABLE IF NOT EXISTS DriverStatus (
                StatusID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS Driver (
                UserID INTEGER PRIMARY KEY,
                LicenseNumber TEXT UNIQUE,
                LicensePlate TEXT UNIQUE NOT NULL,
                VehicleType TEXT,
                Latitude REAL,
                Longitude REAL,
                StatusID INTEGER DEFAULT 1,
                FOREIGN KEY (UserID) REFERENCES Users(UserID),
                FOREIGN KEY (StatusID) REFERENCES DriverStatus(StatusID)
            );
            
            CREATE TABLE IF NOT EXISTS RideStatus (
                StatusID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS Rides (
                RideID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                DriverID INTEGER,
                StatusID INTEGER NOT NULL,
                Fare REAL NOT NULL,
                CancellationFee REAL DEFAULT 0.0,
                CancellationReason TEXT,
                RequestedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PickupTime TIMESTAMP,
                DropoffTime TIMESTAMP,
                PickupLat REAL NOT NULL,
                PickupLon REAL NOT NULL,
                DropoffLat REAL NOT NULL,
                DropoffLon REAL NOT NULL,
                FOREIGN KEY (UserID) REFERENCES Users(UserID),
                FOREIGN KEY (DriverID) REFERENCES Driver(UserID),
                FOREIGN KEY (StatusID) REFERENCES RideStatus(StatusID)
            );
        """)
        
        # Insert default values
        cursor.executescript("""
            INSERT INTO Role (Name) VALUES 
            ('admin'), ('driver'), ('user');
            
            INSERT INTO DriverStatus (Name) VALUES 
            ('offline'), ('available'), ('busy');
            
            INSERT INTO RideStatus (Name) VALUES 
            ('requested'), ('accepted'), ('in_progress'), ('completed'), ('cancelled');
        """)
        
        conn.commit()
        print("Database initialized successfully!")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()
