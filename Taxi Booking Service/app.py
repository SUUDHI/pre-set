from flask import Flask, render_template
from routes.auth_routes import auth_bp
from routes.driver_routes import driver_bp
from routes.ride_routes import ride_bp

app = Flask(__name__, template_folder="templates")

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(driver_bp, url_prefix="/driver")
app.register_blueprint(ride_bp, url_prefix="/ride")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register_user")  
def register_page():
    return render_template("register.html")

@app.route("/register_driver")
def register_driver_page():
    return render_template("register_driver.html")  # Ensure this file exists in 'templates' folder

@driver_bp.route("/driver/login", methods=['GET'])
def driver_login_page():
    return render_template("driver_login.html")

@driver_bp.route("/dashboard")
def driver_dashboard():
    return render_template("driver_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
