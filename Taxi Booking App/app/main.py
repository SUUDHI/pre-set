from flask import Flask, render_template
from routes.auth_routes import auth_bp
from routes.driver_routes import driver_bp
from routes.ride_routes import ride_bp
from utils.config import SECRET_KEY

class TaxiApp:
    def __init__(self):
        self.app = Flask(__name__, template_folder="templates")
        self.app.secret_key = SECRET_KEY 
        self.register_blueprints()
        self.register_routes()

    def register_blueprints(self):
        self.app.register_blueprint(auth_bp, url_prefix="/auth")
        self.app.register_blueprint(driver_bp, url_prefix="/driver")
        self.app.register_blueprint(ride_bp, url_prefix="/ride")

    def register_routes(self):
        @self.app.route("/")
        def home():
            return render_template("index.html")

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    TaxiApp().run()
