import requests
import json
import os

# Get secrets from environment
API_KEY = os.getenv('STEAM_API_KEY')
STEAM_ID = os.getenv('STEAM_ID')

# Steam API endpoint for recently played games
url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}&format=json&count=3"

response = requests.get(url)
data = response.json()

# Save only what we need to keep it "low-profile"
games = []
if "games" in data.get("response", {}):
    for game in data["response"]["games"]:
        games.append({
            "name": game["name"],
            "image": f"https://cdn.akamai.steamstatic.com/steam/apps/{game['appid']}/header.jpg",
        })

with open("recently_played.json", "w") as f:
    json.dump(games, f)