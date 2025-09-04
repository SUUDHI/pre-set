
Taxi Booking App

A backend solution for a taxi booking service that enables users to register, request rides, and get matched with available drivers based on proximity, availability, and preferences. Built with Flask, the project follows SOLID principles, features JWT authentication, and ensures maintainability with a modular structure.

🔧 Features
✅ User & Driver Registration/Login

🔐 JWT Authentication with role-based access (user, driver)

📍 Ride Request System with pickup/dropoff coordination

🧠 Driver Matching based on real-time proximity & availability

💸 Dynamic Fare Calculation using distance

📦 Clean Architecture following SOLID principles

🧪 Easy API testing via Postman

📁 Project Structure
bash
Copy
Edit

## structure
```taxi-booking-app/
├── app/
│   ├── main.py                   
│   │
│   └── templates/
│       └── index.html            
├── routes/
│   ├── auth_routes.py            
│   ├── driver_routes.py          
│   ├── ride_routes.py            
│
├── services/
│   ├── user_service.py           
│   ├── driver_service.py         
│   ├── ride_service.py           
│
├── db_operations/
│   ├── user_ops.py               
│   ├── driver_ops.py             
│   ├── ride_ops.py               
│
├── utils/
│   ├── jwt_handler.py            
│   ├── jwt_utils.py              
│   ├── validators.py             
│   ├── distance.py               
│   ├── fare.py                   
│   ├── config.py                 
│   ├── coordinate.py             
│
├── db/
│   ├── connect_db.py             
│   ├── initialize_db.py          
│     
│
└── taxi_booking.db                
├── run.py                        
└── README.md                    
```

🚀 Getting Started
```
✅ Requirements
Python 3.9+

Flask

SQLite (default, no setup needed)
```