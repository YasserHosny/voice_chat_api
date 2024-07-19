from app import create_app

print("Starting application...")

app = create_app()

if __name__ == "__main__":
    print("Running application on http://0.0.0.0:5020")
    app.run(host="0.0.0.0", port=5020, debug=True)
