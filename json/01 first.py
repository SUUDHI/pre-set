import json

with open("01_data.json","r") as file:
    data = json.load(file)

print(data)
print(type(data))
print("Name:", data["Emp"]["name"])
print("Age:", data["Emp"]["age"])
