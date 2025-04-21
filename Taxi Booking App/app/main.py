from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.ride_routes import ride_bp
from routes.driver_routes import driver_bp

class TaxiApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["JSON_SORT_KEYS"] = False
        CORS(self.app)  # Enable CORS for all routes
        self.register_blueprints()

    def register_blueprints(self):
        self.app.register_blueprint(auth_bp, url_prefix="/auth")
        self.app.register_blueprint(ride_bp, url_prefix="/ride")
        self.app.register_blueprint(driver_bp, url_prefix="/driver")

    def run(self):
        self.app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    TaxiApp().run()
