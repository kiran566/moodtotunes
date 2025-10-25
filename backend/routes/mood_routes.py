from flask import Blueprint, request, jsonify
from services.sentiment_service import detect_mood
from services.spotify_service import get_spotify_recommendations
from models.user_mood import db, UserMood
# Import JWT tools:
from flask_jwt_extended import jwt_required, get_jwt_identity

mood_routes = Blueprint('mood_routes', __name__)

@mood_routes.route('/analyze', methods=['POST'])
@jwt_required() # <-- Protect the route
def analyze_mood():
    data = request.get_json()
    user_text = data.get("text", "")
    
    # Get market/language from user input (for Mod #2)
    market = data.get("market", None) # e.g., "ES", "FR", "JP"

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # Get the user ID from their token
    current_user_id = get_jwt_identity()

    # Detect sentiment
    sentiment = detect_mood(user_text)

    # Fetch Spotify recommendations (pass market for Mod #2)
    songs = get_spotify_recommendations(sentiment, market)

    # Save to database, linking to the user
    entry = UserMood(text=user_text, sentiment=sentiment, user_id=current_user_id)
    db.session.add(entry)
    db.session.commit()

    return jsonify({
        "sentiment": sentiment,
        "songs": songs
    })

@mood_routes.route('/history', methods=['GET'])
@jwt_required() # <-- Protect the route
def get_history():
    # Get the user ID from their token
    current_user_id = get_jwt_identity()

    # Fetch history only for the currently logged-in user
    moods = UserMood.query.filter_by(user_id=current_user_id)\
                          .order_by(UserMood.timestamp.desc())\
                          .limit(10).all()
    
    return jsonify([m.to_dict() for m in moods])