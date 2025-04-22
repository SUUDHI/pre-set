from app.main import TaxiApp

if __name__ == "__main__":
    app = TaxiApp().app
    app.run(host='0.0.0.0', port=5000, debug=True)
