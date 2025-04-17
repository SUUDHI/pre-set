import unittest
import requests
import json
from datetime import datetime
import sqlite3
from db.connect_db import DatabaseConnector

class TestDriverAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    
    def setUp(self):
        """Set up test data"""
        print("\nSetting up test data...")
        self.test_driver = {
            "name": "Test Driver",
            "phone": "9876543210",
            "email": f"test.driver{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "testpassword123",
            "birth": "1990-01-01",
            "license_plate": f"TEST{datetime.now().strftime('%H%M%S')}",
            "gender": "M"
        }
        print(f"Test driver email: {self.test_driver['email']}")
        print(f"Test license plate: {self.test_driver['license_plate']}")
    
    def test_1_register_driver_success(self):
        """Test successful driver registration"""
        print("\nTesting driver registration...")
        try:
            response = requests.post(f"{self.BASE_URL}/driver/register", json=self.test_driver)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertIn("message", data)
            self.assertIn("driver_id", data)
            self.assertEqual(data["message"], "Driver registered successfully")
            
            # Store driver_id for later tests
            self.driver_id = data["driver_id"]
            print(f"Driver registered successfully with ID: {self.driver_id}")
        except Exception as e:
            print(f"Error in test_1_register_driver_success: {str(e)}")
            raise
    
    def test_2_register_driver_duplicate_email(self):
        """Test registration with duplicate email"""
        print("\nTesting duplicate email registration...")
        try:
            response = requests.post(f"{self.BASE_URL}/driver/register", json=self.test_driver)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertIn("error", data)
            self.assertIn("Email already exists", data["error"])
        except Exception as e:
            print(f"Error in test_2_register_driver_duplicate_email: {str(e)}")
            raise
    
    def test_3_register_driver_missing_fields(self):
        """Test registration with missing required fields"""
        print("\nTesting registration with missing fields...")
        try:
            invalid_data = self.test_driver.copy()
            del invalid_data["license_plate"]
            print(f"Test data with missing license_plate: {invalid_data}")
            
            response = requests.post(f"{self.BASE_URL}/driver/register", json=invalid_data)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertIn("error", data)
            self.assertIn("Missing or empty required field", data["error"])
        except Exception as e:
            print(f"Error in test_3_register_driver_missing_fields: {str(e)}")
            raise
    
    def test_4_login_driver_success(self):
        """Test successful driver login"""
        print("\nTesting driver login...")
        try:
            login_data = {
                "email": self.test_driver["email"],
                "password": self.test_driver["password"]
            }
            print(f"Login attempt with email: {login_data['email']}")
            
            response = requests.post(f"{self.BASE_URL}/driver/login", json=login_data)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("token", data)
            self.assertIn("driver_id", data)
            
            # Store token for later tests
            self.token = data["token"]
            print("Login successful, token received")
        except Exception as e:
            print(f"Error in test_4_login_driver_success: {str(e)}")
            raise
    
    def test_5_login_driver_invalid_credentials(self):
        """Test login with invalid credentials"""
        print("\nTesting login with invalid credentials...")
        try:
            login_data = {
                "email": self.test_driver["email"],
                "password": "wrongpassword"
            }
            print(f"Login attempt with wrong password for email: {login_data['email']}")
            
            response = requests.post(f"{self.BASE_URL}/driver/login", json=login_data)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            self.assertEqual(response.status_code, 401)
            data = response.json()
            self.assertIn("error", data)
            self.assertEqual(data["error"], "Invalid credentials")
        except Exception as e:
            print(f"Error in test_5_login_driver_invalid_credentials: {str(e)}")
            raise
    
    def test_6_update_driver_location(self):
        """Test updating driver location"""
        print("\nTesting driver location update...")
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            location_data = {
                "latitude": 12.9716,
                "longitude": 77.5946
            }
            print(f"Updating location with data: {location_data}")
            
            response = requests.put(
                f"{self.BASE_URL}/driver/location",
                json=location_data,
                headers=headers
            )
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("message", data)
            self.assertEqual(data["message"], "Location updated successfully")
        except Exception as e:
            print(f"Error in test_6_update_driver_location: {str(e)}")
            raise

    def test_7_update_driver_status(self):
        """Test updating driver status"""
        print("\nTesting driver status update...")
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            status_data = {"status": "available"}
            print(f"Updating status with data: {status_data}")
            
            response = requests.put(
                f"{self.BASE_URL}/driver/status",
                json=status_data,
                headers=headers
            )
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("message", data)
            self.assertEqual(data["message"], "Status updated successfully")

            # Test invalid status
            status_data = {"status": "invalid_status"}
            response = requests.put(
                f"{self.BASE_URL}/driver/status",
                json=status_data,
                headers=headers
            )
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertIn("error", data)
            self.assertIn("Invalid status", data["error"])
        except Exception as e:
            print(f"Error in test_7_update_driver_status: {str(e)}")
            raise

def register_driver_directly(driver_data):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    
    try:
        # First insert into User table
        cursor.execute("""
            INSERT INTO User (Name, Email, Password, RoleID)
            VALUES (?, ?, ?, ?)
        """, (driver_data["name"], driver_data["email"], driver_data["password"], 2))  # Assuming 2 is driver role
        
        user_id = cursor.lastrowid
        
        # Then insert into Driver table
        cursor.execute("""
            INSERT INTO Driver (UserID, LicensePlate, StatusID)
            VALUES (?, ?, ?)
        """, (user_id, driver_data["license_plate"], 1))  # Assuming 1 is available status
        
        conn.commit()
        print("Driver registered successfully!")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print("Error registering driver:", str(e))
        conn.rollback()
        return None
    finally:
        conn.close()

# Example usage
driver_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "license_plate": "ABC123"
}

driver_id = register_driver_directly(driver_data)
if driver_id:
    print("Driver ID:", driver_id)

def check_driver_registration(email):
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.UserID, u.Name, u.Email, d.DriverID, d.LicensePlate
        FROM User u
        JOIN Driver d ON u.UserID = d.UserID
        WHERE u.Email = ?
    """, (email,))
    
    driver = cursor.fetchone()
    conn.close()
    
    if driver:
        print("Driver found:")
        print(f"User ID: {driver[0]}")
        print(f"Name: {driver[1]}")
        print(f"Email: {driver[2]}")
        print(f"Driver ID: {driver[3]}")
        print(f"License Plate: {driver[4]}")
    else:
        print("Driver not found")

# Check the registration
check_driver_registration("john.doe@example.com")

if __name__ == "__main__":
    unittest.main() 