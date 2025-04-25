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
            DROP TABLE IF EXISTS VehicleTypes;
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
            
            CREATE TABLE IF NOT EXISTS VehicleTypes (
                VehicleTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT UNIQUE NOT NULL,
                Description TEXT,
                BaseRate REAL NOT NULL,
                PricePerKm REAL NOT NULL,
                MaxPassengers INTEGER NOT NULL,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS DriverStatus (
                StatusID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS Driver (
                UserID INTEGER PRIMARY KEY,
                LicenseNumber TEXT UNIQUE,
                LicensePlate TEXT UNIQUE NOT NULL,
                VehicleTypeID INTEGER NOT NULL,
                Latitude REAL,
                Longitude REAL,
                StatusID INTEGER DEFAULT 1,
                FOREIGN KEY (UserID) REFERENCES Users(UserID),
                FOREIGN KEY (StatusID) REFERENCES DriverStatus(StatusID),
                FOREIGN KEY (VehicleTypeID) REFERENCES VehicleTypes(VehicleTypeID)
            );
            
            CREATE TABLE IF NOT EXISTS RideStatus (
                StatusID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT UNIQUE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS Rides (
                RideID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                DriverID INTEGER,
                VehicleTypeID INTEGER NOT NULL,
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
                FOREIGN KEY (StatusID) REFERENCES RideStatus(StatusID),
                FOREIGN KEY (VehicleTypeID) REFERENCES VehicleTypes(VehicleTypeID)
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
            
            INSERT INTO VehicleTypes (Name, Description, BaseRate, PricePerKm, MaxPassengers) VALUES 
            ('Sedan', '4-door car, comfortable for up to 4 passengers', 50.00, 12.00, 4),
            ('SUV', 'Spacious vehicle, ideal for 6 passengers', 70.00, 15.00, 6),
            ('Luxury', 'Premium vehicle with high-end amenities', 100.00, 20.00, 4),
            ('Compact', 'Economic choice for 1-3 passengers', 40.00, 10.00, 3);
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
