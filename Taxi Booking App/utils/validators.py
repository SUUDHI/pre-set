def validate_user_data(data, required_fields):
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    return True, "Valid"

def validate_driver_data(data, required_fields):
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    return True, "Valid"

def validate_ride_data(data, required_fields):
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    return True, "Valid"
