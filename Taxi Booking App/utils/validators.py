def validate_required_fields(data, required_fields):
    """
    Generic validator for checking presence and non-empty values of required fields.
    """
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing or empty required field: {field}"
    return True, None


def validate_user_data(data):
    required_fields = ["name", "email", "phone", "password", "role"]
    return validate_required_fields(data, required_fields)


def validate_login_data(data):
    required_fields = ["email", "password"]
    return validate_required_fields(data, required_fields)


def validate_ride_data(data):
    """
    Validates the ride request data.
    Required fields are pickup and dropoff coordinates.
    """
    required_fields = ["pickup_lat", "pickup_lon", "dropoff_lat", "dropoff_lon"]
    return validate_required_fields(data, required_fields)


def validate_driver_location_data(data):
    required_fields = ["latitude", "longitude"]
    return validate_required_fields(data, required_fields)


def validate_driver_data(data, required_fields):
    """
    Validates driver registration data.
    """
    return validate_required_fields(data, required_fields)
