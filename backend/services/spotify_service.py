import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from utils.config import Config

# Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=Config.SPOTIFY_CLIENT_ID,
    client_secret=Config.SPOTIFY_CLIENT_SECRET
))

def get_spotify_recommendations(sentiment: str):
    """Return list of Spotify tracks based on sentiment."""
    if sentiment == "POSITIVE":
        query = "happy"
    elif sentiment == "NEGATIVE":
        query = "sad"
    else:
        query = "chill"

    tracks = sp.search(q=query, type="track", limit=5)
    return [
        {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"]
        }
        for t in tracks["tracks"]["items"]
    ]
