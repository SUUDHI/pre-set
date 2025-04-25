import requests
import json
import time

BASE_URL = "http://localhost:5000"

def register_driver(driver_data):
    response = requests.post(
        f"{BASE_URL}/driver/register",
        json=driver_data
    )
    print(f"Registering driver {driver_data['name']}: {response.status_code}")
    print(response.json())
    return response.json()

def register_user(user_data):
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )
    print(f"Registering user {user_data['name']}: {response.status_code}")
    print(response.json())
    return response.json()

def create_ride_request(ride_data, token):
    response = requests.post(
        f"{BASE_URL}/ride/request",
        json=ride_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Creating ride request: {response.status_code}")
    print(response.json())
    return response.json()

def create_ride_requests():
    """Create sample ride requests"""
    ride_data = [
        {
            "pickup_lat": 40.7128,
            "pickup_lon": -74.0060,
            "dropoff_lat": 40.7589,
            "dropoff_lon": -73.9851,
            "vehicle_type_id": 1  # Standard
        },
        {
            "pickup_lat": 40.7589,
            "pickup_lon": -73.9851,
            "dropoff_lat": 40.7829,
            "dropoff_lon": -73.9654,
            "vehicle_type_id": 2  # Premium
        },
        {
            "pickup_lat": 40.7829,
            "pickup_lon": -73.9654,
            "dropoff_lat": 40.7128,
            "dropoff_lon": -74.0060,
            "vehicle_type_id": 3  # Van
        }
    ]

    for ride in ride_data:
        try:
            response = requests.post(
                f"{BASE_URL}/rides/request",
                headers={"Authorization": f"Bearer {USER_TOKEN}"},
                json=ride
            )
            print(f"Ride request response: {response.status_code}")
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error creating ride request: {e}")

# Test Data
drivers = [
    {
        "name": "John Sedan",
        "email": "john.sedan@example.com",
        "phone": "+1234567890",
        "password": "password123",
        "birth": "1990-01-01",
        "gender": "male",
        "licensePlate": "SED123",
        "vehicleTypeId": 1,  # Sedan
        "role": "driver"
    },
    {
        "name": "Sarah SUV",
        "email": "sarah.suv@example.com",
        "phone": "+1234567891",
        "password": "password123",
        "birth": "1992-02-02",
        "gender": "female",
        "licensePlate": "SUV456",
        "vehicleTypeId": 2,  # SUV
        "role": "driver"
    },
    {
        "name": "Mike Luxury",
        "email": "mike.luxury@example.com",
        "phone": "+1234567892",
        "password": "password123",
        "birth": "1985-03-03",
        "gender": "male",
        "licensePlate": "LUX789",
        "vehicleTypeId": 3,  # Luxury
        "role": "driver"
    }
]

users = [
    {
        "name": "User One",
        "email": "user1@example.com",
        "phone": "+9876543210",
        "password": "password123",
        "birth": "1995-01-01",
        "gender": "male",
        "role": "user"
    },
    {
        "name": "User Two",
        "email": "user2@example.com",
        "phone": "+9876543211",
        "password": "password123",
        "birth": "1995-02-02",
        "gender": "female",
        "role": "user"
    }
]

# Register drivers
print("Registering drivers...")
for driver in drivers:
    register_driver(driver)
    time.sleep(1)  # Add delay between requests

# Register users
print("\nRegistering users...")
for user in users:
    register_user(user)
    time.sleep(1)

# Login as a user to get token
print("\nLogging in as user...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "user1@example.com",
        "password": "password123"
    }
)
user_token = login_response.json().get("token")

if user_token:
    # Create ride requests for different vehicle types
    ride_requests = [
        {
            "pickup_lat": 12.9716,
            "pickup_lon": 77.5946,
            "dropoff_lat": 13.0827,
            "dropoff_lon": 77.5877,
            "vehicle_type_id": 1  # Sedan
        },
        {
            "pickup_lat": 12.9716,
            "pickup_lon": 77.5946,
            "dropoff_lat": 13.0827,
            "dropoff_lon": 77.5877,
            "vehicle_type_id": 2  # SUV
        },
        {
            "pickup_lat": 12.9716,
            "pickup_lon": 77.5946,
            "dropoff_lat": 13.0827,
            "dropoff_lon": 77.5877,
            "vehicle_type_id": 3  # Luxury
        }
    ]
    
    print("\nCreating ride requests...")
    for ride in ride_requests:
        create_ride_request(ride, user_token)
        time.sleep(1)

print("\nTest data creation completed!") 