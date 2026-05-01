import json
import os

BASE_DIR = os.path.dirname(__file__)
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": [255, 255, 255],
    "difficulty": "normal",
    "car_type": "Sport"
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
        except: pass
    return dict(DEFAULT_SETTINGS)

def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except: pass
    return []

def save_score(name: str, score: int, distance: int):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": distance})
    lb = sorted(lb, key=lambda x: x["score"], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f, indent=2)