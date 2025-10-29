import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from utils.config import Config

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=Config.SPOTIFY_CLIENT_ID,
    client_secret=Config.SPOTIFY_CLIENT_SECRET
))

# Mood-to-keyword mapping
MOOD_KEYWORDS = {
    "JOY": ["happy", "feel good", "celebration", "dance", "smile"],
    "SADNESS": ["sad", "melancholy", "broken heart", "emotional", "lonely"],
    "ANGER": ["rage", "rock", "angry", "metal"],
    "LOVE": ["romantic", "love songs", "soft music"],
    "FEAR": ["dark", "mystery", "chill", "intense"],
    "SURPRISE": ["party", "energetic", "pop"],
    "NEUTRAL": ["chill", "relax", "ambient", "lofi"]
}

# Supported Indian languages
LANGUAGE_KEYWORDS = ["hindi", "telugu", "tamil", "malayalam", "kannada"]

def get_spotify_recommendations(sentiment: str):
    """Fetch randomized Spotify tracks based on mood and regional language."""
    mood = sentiment.upper()
    mood_queries = MOOD_KEYWORDS.get(mood, ["mood"])
    selected_mood = random.choice(mood_queries)
    selected_lang = random.choice(LANGUAGE_KEYWORDS)

    # Build final search query
    query = f"{selected_mood} {selected_lang}"

    tracks = sp.search(q=query, type="track", limit=10)
    return [
        {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"],
            "preview_url": t["preview_url"]
        }
        for t in tracks["tracks"]["items"]
    ]
