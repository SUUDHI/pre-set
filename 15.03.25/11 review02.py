data = {
    "user": {
        "name": "Alice",
        "details": {
            "emails": ["alice@example.com", "a.smith@example.com"],
            "address": {"city": "Wonderland", "zip": 12345}
        }
    }
}
print(data["user"]["details"]["address"]["city"][::-1])

#dnalrednoW grting city name in return in reverse because by using ([]) we reaches to the city value then reverse it. 