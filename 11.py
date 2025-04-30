data = {
  "user": {
       "name": "Alice",
      "details": {
           "emails": ["alice@example.com", "a.smith@example.com"],
           "address": {"city": "Weather is Awesome", "zip": 12345}
       }
   }
 }
print(data["user"]["details"]["address"]["city"][:5:-1])
# htaew