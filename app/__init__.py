from flask import Flask

def create_app():
    print("Creating Flask application...")
    app = Flask(__name__)

    from app.api.voice import voice_bp
    app.register_blueprint(voice_bp, url_prefix='/api/voice')

    print("Application created and blueprint registered.")
    return app
