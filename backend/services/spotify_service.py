# services/spotify_service.py
import spotipy
import random # <-- Import random
from spotipy.oauth2 import SpotifyClientCredentials
from utils.config import Config

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=Config.SPOTIFY_CLIENT_ID,
    client_secret=Config.SPOTIFY_CLIENT_SECRET
))

def get_spotify_recommendations(sentiment: str, market: str = None):
    if sentiment == "POSITIVE":
        query = "happy"
    elif sentiment == "NEGATIVE":
        query = "sad"
    else:
        query = "chill"

    # --- Start of Randomization Logic ---
    
    # 1. Get a random offset to search deeper in Spotify's results
    # (e.g., pick a starting point between 0 and 200)
    # Note: Spotify results get less relevant after ~1000
    random_offset = random.randint(0, 200)

    # 2. Search for a large batch of tracks (max 50) at that offset
    tracks_result = sp.search(
        q=query, 
        type="track", 
        limit=50, # Get a big list
        offset=random_offset, # Start at a random spot
        market=market # Use the market code from user
    )
    
    all_tracks = tracks_result["tracks"]["items"]

    if not all_tracks:
        return [] # No tracks found

    # 3. Pick 5 random tracks *from that batch*
    # Use min() in case Spotify returns fewer than 5 tracks
    num_to_select = min(5, len(all_tracks))
    selected_tracks = random.sample(all_tracks, num_to_select)

    # --- End of Randomization Logic ---

    # 4. Format the final list
    return [
       {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"],
            "preview_url": t["preview_url"]
        }
        for t in selected_tracks
   ]