from flask import Flask
from flask_cors import CORS
from config import Config

# Initialize Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for frontend communication
    
    with app.app_context():
        from database import init_db
        init_db()  # Ensure database is initialized
    
    return app
