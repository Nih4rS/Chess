import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

LICHESS_TOKEN = os.getenv("LICHESS_TOKEN")
HEADERS = {'Authorization': f'Bearer {LICHESS_TOKEN}'}

def fetch_games(username, max_games=10):
    url = f'https://lichess.org/api/games/user/{username}'
    params = {
        'max': max_games,
        'pgnInJson': True,
        'moves': True,
        'tags': True,
        'clocks': True,
        'evals': True
    }
    response = requests.get(url, headers=HEADERS, params=params, stream=True)
    response.raise_for_status()

    games = []
    for line in response.iter_lines():
        if line:
            game_data = json.loads(line)
            games.append(game_data)

    return games

def save_games_to_file(games, filename):
    with open(filename, 'w') as f:
        json.dump(games, f, indent=4)

if __name__ == "__main__":
    username = 'MagnusCarlsen'  # Change this username
    games = fetch_games(username)
    save_games_to_file(games, '../data/raw/games.json')
    print(f"Fetched and saved {len(games)} games.")
