from flask import Blueprint, request, jsonify
from services.sentiment_service import detect_mood
from services.spotify_service import get_spotify_recommendations
from models.user_mood import db, UserMood

mood_routes = Blueprint('mood_routes', __name__)

@mood_routes.route('/analyze', methods=['POST'])
def analyze_mood():
    """Analyze mood text and return Spotify song recommendations."""
    data = request.get_json()
    user_text = data.get("text", "")

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # 1️⃣ Detect sentiment
    sentiment = detect_mood(user_text)

    # 2️⃣ Fetch Spotify recommendations
    songs = get_spotify_recommendations(sentiment)

    # 3️⃣ Save to database
    entry = UserMood(text=user_text, sentiment=sentiment)
    db.session.add(entry)
    db.session.commit()

    return jsonify({
        "sentiment": sentiment,
        "songs": songs
    })

@mood_routes.route('/history', methods=['GET'])
def get_history():
    """Get last 10 mood entries."""
    moods = UserMood.query.order_by(UserMood.timestamp.desc()).limit(10).all()
    return jsonify([m.to_dict() for m in moods])
