from app.main import TaxiApp
from waitress import serve

application = TaxiApp().app  # <-- Important for IIS

if __name__ == "__main__":
    print("Starting server on http://192.168.29.37:5000")
    serve(application, host="192.168.29.37", port=5006)
