def _validate_generic(data, required_fields):
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    return True, "All required fields are present."

def validate_user_data(data, required_fields):
    return _validate_generic(data, required_fields)

def validate_driver_data(data, required_fields):
    return _validate_generic(data, required_fields)

def validate_ride_data(data, required_fields):
    return _validate_generic(data, required_fields)
