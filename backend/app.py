from flask import Flask
from flask_cors import CORS
from models.user_mood import db
from models.user import bcrypt # <-- Import bcrypt
from routes.mood_routes import mood_routes
from routes.auth_routes import auth_routes # <-- Import auth routes
from utils.config import Config
from flask_jwt_extended import JWTManager # <-- Import JWT

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Add a JWT_SECRET_KEY to your Config
    # This is *required* for JWT.
    # Go to your config.py and add:
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'a_very_strong_default_secret_key')
    # Make sure to set JWT_SECRET_KEY in your .env file
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY 
    
    CORS(app)
    JWTManager(app) # <-- Initialize JWT
    bcrypt.init_app(app) # <-- Initialize Bcrypt
    db.init_app(app)

    app.register_blueprint(mood_routes, url_prefix='/api')
    app.register_blueprint(auth_routes, url_prefix='/api/auth') # <-- Register auth routes

    with app.app_context():
        db.create_all() 

    @app.route('/')
    def home():
        return {"message": "Welcome to MoodTunes API (Flask + SQLite)"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)