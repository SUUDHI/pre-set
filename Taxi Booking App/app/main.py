from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.ride_routes import ride_bp
from routes.driver_routes import driver_bp
import os

class TaxiApp:
    def __init__(self):
        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
        self.app = Flask(__name__, 
                        template_folder=template_dir,
                        static_folder=static_dir)
        self.app.config["JSON_SORT_KEYS"] = False
        CORS(self.app)  # Enable CORS for all routes
        self.register_blueprints()
        self.register_routes()

    def register_blueprints(self):
        self.app.register_blueprint(auth_bp, url_prefix="/auth")
        self.app.register_blueprint(ride_bp, url_prefix="/rides")
        self.app.register_blueprint(driver_bp, url_prefix="/driver")

    def register_routes(self):
        @self.app.route("/")
        def home():
            return render_template("index.html")

        @self.app.route("/static/<path:path>")
        def serve_static(path):
            return send_from_directory('static', path)

        @self.app.route("/driver/dashboard")
        def driver_dashboard():
            return render_template("driver_dashboard.html")

        @self.app.route("/dashboard")
        def user_dashboard():
            return render_template("dashboard.html")

    def run(self):
        self.app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    TaxiApp().run()
