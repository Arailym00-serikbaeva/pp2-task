import json  # JSON файлдарымен жұмыс істеуге арналған кітапхананы қосу
import os    # Файлдар мен папкалардың жолдарын басқаруға арналған кітапхананы қосу

# Ағымдағы файл орналасқан папканың толық жолын алу
BASE_DIR = os.path.dirname(__file__)

# Лидерлер кестесі (leaderboard.json) файлына баратын толық жолды құрастыру
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

# Баптаулар (settings.json) файлына баратын толық жолды құрастыру
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# Егер файл табылмаса немесе жаңа болса, қолданылатын стандартты баптаулар
DEFAULT_SETTINGS = {
    "sound": True,              # Дыбыс қосулы/өшірулі
    "car_color": [255, 255, 255], # Көліктің түсі (RGB форматында)
    "difficulty": "normal",      # Ойын қиындығы
    "car_type": "Sport"         # Көлік түрі
}

# Баптауларды файлдан жүктейтін функция
def load_settings():
    # Егер файл бар болса
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f: # Файлды оқу ("r") режимінде ашу
                data = json.load(f)             # JSON деректерін Python сөздігіне айналдыру
            
            # Файлда кейбір баптаулар жоқ болса, оларды DEFAULT_SETTINGS-тен қосу
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
        except: pass # Қате кетсе (мысалы, файл бос болса), ештеңе істемей келесіге өту
    
    # Егер файл жоқ болса немесе қате болса, стандартты баптаулардың көшірмесін қайтару
    return dict(DEFAULT_SETTINGS)

# Баптауларды файлға сақтайтын функция
def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w") as f:        # Файлды жазу ("w") режимінде ашу
        # Сөздікті файлға ыңғайлы форматта (шегініспен) JSON қылып жазу
        json.dump(settings, f, indent=2)

# Лидерлер кестесін жүктейтін функция
def load_leaderboard():
    # Егер файл бар болса
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f) # Нәтижені тізім ретінде қайтару
        except: pass
    return [] # Егер файл болмаса, бос тізім қайтару

# Жаңа нәтижені сақтайтын функция
def save_score(name: str, score: int, distance: int):
    lb = load_leaderboard() # Қазіргі кестені жүктеп алу
    # Жаңа ойыншының мәліметтерін тізімге қосу
    lb.append({"name": name, "score": score, "distance": distance})
    
    # Ұпай (score) бойынша кему ретімен сұрыптау және тек үздік 10 нәтижені қалдыру
    lb = sorted(lb, key=lambda x: x["score"], reverse=True)[:10]
    
    # Жаңартылған тізімді файлға қайта жазу
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f, indent=2)