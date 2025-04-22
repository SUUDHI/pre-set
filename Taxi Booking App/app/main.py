from flask import Flask, render_template
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.ride_routes import ride_bp
from routes.driver_routes import driver_bp
import os

class TaxiApp:
    def __init__(self):
        self.app = Flask(__name__, 
                        template_folder='../templates',
                        static_folder='../static',
                        static_url_path='')
        self.app.config["JSON_SORT_KEYS"] = False
        self.app.config['SECRET_KEY'] = 'your-secret-key'
        CORS(self.app)
        self.register_blueprints()
        self.register_routes()

    def register_blueprints(self):
        self.app.register_blueprint(auth_bp, url_prefix="/auth")
        self.app.register_blueprint(ride_bp, url_prefix="/ride")
        self.app.register_blueprint(driver_bp, url_prefix="/driver")

    def register_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/user-dashboard')
        def user_dashboard():
            return render_template('user-dashboard.html')

        @self.app.route('/driver-dashboard')
        def driver_dashboard():
            return render_template('driver-dashboard.html')

if __name__ == "__main__":
    app = TaxiApp().app
    app.run()
