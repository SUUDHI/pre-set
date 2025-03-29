from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user storage
users = {}

# GET User by ID
@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({"user_id": user_id, "data": user})
    return jsonify({"error": "User not found"}), 404

# POST: Add New User
@app.route("/add-user", methods=["POST"])
def add_user():
    data = request.get_json()
    if "id" not in data or "name" not in data or "age" not in data:
        return jsonify({"error": "Missing fields"}), 400

    user_id = data["id"]
    if user_id in users:
        return jsonify({"error": "User already exists"}), 409

    users[user_id] = {"name": data["name"], "age": data["age"]}
    return jsonify({"message": "User added successfully!", "user": users[user_id]}), 201

# PUT: Update User
@app.route("/update-user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "name" not in data or "age" not in data:
        return jsonify({"error": "Missing fields"}), 400

    users[user_id]["name"] = data["name"]
    users[user_id]["age"] = data["age"]

    return jsonify({"message": "User updated successfully", "user": users[user_id]}), 200

# DELETE: Remove User
@app.route("/delete-user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
