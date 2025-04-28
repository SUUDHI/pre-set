from flask_socketio import SocketIO, emit, join_room, leave_room
from utils.jwt_handler import jwt_handler
import json

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_ride')
def handle_join_ride(data):
    try:
        # Verify JWT token
        token = data.get('token')
        if not token:
            emit('error', {'message': 'Authentication required'})
            return

        user_data = jwt_handler.verify_token(token)
        if not user_data:
            emit('error', {'message': 'Invalid token'})
            return

        ride_id = data.get('ride_id')
        if not ride_id:
            emit('error', {'message': 'Ride ID required'})
            return

        # Join the room for this specific ride
        join_room(f'ride_{ride_id}')
        emit('joined_ride', {'message': f'Joined ride room {ride_id}'})

    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('leave_ride')
def handle_leave_ride(data):
    try:
        ride_id = data.get('ride_id')
        if ride_id:
            leave_room(f'ride_{ride_id}')
            emit('left_ride', {'message': f'Left ride room {ride_id}'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('driver_location_update')
def handle_driver_location(data):
    try:
        # Verify JWT token
        token = data.get('token')
        if not token:
            emit('error', {'message': 'Authentication required'})
            return

        user_data = jwt_handler.verify_token(token)
        if not user_data or user_data.get('role') != 'driver':
            emit('error', {'message': 'Invalid token or unauthorized'})
            return

        ride_id = data.get('ride_id')
        location = data.get('location')
        
        if not ride_id or not location:
            emit('error', {'message': 'Ride ID and location required'})
            return

        # Broadcast location update to all clients in the ride room
        emit('location_update', {
            'driver_id': user_data.get('user_id'),
            'location': location
        }, room=f'ride_{ride_id}')

    except Exception as e:
        emit('error', {'message': str(e)}) 