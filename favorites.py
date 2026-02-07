import json
from datetime import datetime

def add_to_favorites(user_data):
    favorites = load_favorites()
    favorites.append(user_data)
    save_favorites(favorites)

def get_favorites():
    return load_favorites()

def load_favorites():
    try:
        with open('favorites.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_favorites(data):
    with open('favorites.json', 'w') as file:
        json.dump(data, file, indent=4)
