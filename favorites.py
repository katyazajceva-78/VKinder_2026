import json
import os
from datetime import datetime

FILENAME = "favorites.json"

def load_favorites():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_favorites(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_to_favorites(user_data):
    favorites = load_favorites()
    if any(user["user_id"] == user_data["user_id"] for user in favorites):
        return False
    user_data["added_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    favorites.append(user_data)
    save_favorites(favorites)
    return True
