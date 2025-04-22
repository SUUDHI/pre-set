from app.main import TaxiApp
from waitress import serve

app = TaxiApp().app

if __name__ == "__main__":
    print("Starting server on http://192.168.29.37:5000")
    serve(app, host="192.168.29.37", port=5000) 