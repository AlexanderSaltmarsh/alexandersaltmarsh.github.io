import os
import requests
import json

# These look for the secrets you just saved in GitHub Settings
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN")

def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    response = requests.post(auth_url, data={
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    return response.json().get("access_token")

def get_top_artists(token):
    # 'short_term' = last 4 weeks. Use 'medium_term' for 6 months.
    url = "https://api.spotify.com/v1/me/top/artists?limit=3&time_range=short_term"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("items", [])

if __name__ == "__main__":
    token = get_access_token()
    artists = get_top_artists(token)
    
    formatted_artists = []
    for artist in artists:
        formatted_artists.append({
            "name": artist["name"],
            "url": artist["external_urls"]["spotify"],
            "image": artist["images"][0]["url"] if artist["images"] else None
        })
        
    with open("spotify_data.json", "w") as f:
        json.dump(formatted_artists, f, indent=4)