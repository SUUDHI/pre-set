from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data ={
        "user id " : user_id,
        "name" : "sudhanshu",
        "age" : 20
    }
    return jsonify(user_data),200

@app.route("/create-user", methods = ["POST"])
def create_user():
    data = request.get_json()

    return jsonify(data),200


@app.route("/check-prime/<int:num>", methods=["GET"])
def check_prime(num):
    result = {
        "number": num,
        "is_prime": is_prime(num)
    }
    return jsonify(result)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):  
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    app.run(debug = True) 
