from flask import Flask
from flask_cors import CORS
from models.user_mood import db
from routes.mood_routes import mood_routes
from utils.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    app.register_blueprint(mood_routes, url_prefix='/api')

    with app.app_context():
        db.create_all()  # Create tables if not exist

    @app.route('/')
    def home():
        return {"message": "Welcome to MoodTunes API (Flask + SQLite)"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
