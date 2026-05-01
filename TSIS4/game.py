import pygame
import random
import db

# Константалар: блоктың өлшемі және ойын алаңының ені мен биіктігі
BLOCK = 20
WIDTH = 600
GAME_HEIGHT = 600 

class Game:
    def __init__(self, username, settings):
        """Ойынды бастапқы іске қосу (Инициализация)"""
        self.username = username
        self.settings = settings
        # Базадан ойыншының ID-ін және жеке рекордын (PB) алу
        self.player_id = db.get_or_create_player(username)
        self.pb = db.get_personal_best(self.player_id)
        self.reset() # Ойынның барлық мәндерін бастапқы күйге келтіру

    def reset(self):
        """Ойынды басынан бастау (Жылан өлгенде немесе жаңадан бастағанда)"""
        self.snake = [[300, 300], [280, 300], [260, 300]] # Жыланның бастапқы денесі
        self.direction = "RIGHT" # Бастапқы бағыты
        self.score = 0           # Ұпай
        self.level = 1           # Деңгей
        self.base_speed = 7      # Негізгі жылдамдық
        self.speed_mod = 0       # Бонустардан келетін жылдамдық өзгерісі
        self.obstacles = []      # Кедергілер тізімі
        self.food = self.spawn_item("normal")  # Кәдімгі тамақ
        self.poison = self.spawn_item("poison") # У (жыланды қысқартады)
        self.powerup = None      # Арнайы бонус (алғашқыда жоқ)
        
        # Бонустың шығу уақытын белгілеу (5-10 секунд аралығында)
        self.pu_spawn_time = pygame.time.get_ticks() + random.randint(5000, 10000)
        self.active_pu_end = 0   # Бонустың әсері бітетін уақыт
        self.shield_active = False # Қорғаныс қалқаны қосулы ма?

    def spawn_item(self, itype):
        """Экранның кездейсоқ жерінен тамақ, у немесе бонус шығару"""
        while True:
            x = random.randrange(0, WIDTH, BLOCK)
            y = random.randrange(0, GAME_HEIGHT, BLOCK)
            pos = [x, y]
            
            # Элемент жыланның үстіне немесе кедергіге түспеуі керек
            if pos not in self.snake and pos not in self.obstacles:
                if itype == "normal":
                    # Кәдімгі тамақ: 70% қызыл (1 ұпай), 20% көк (3 ұпай), 10% алтын (5 ұпай)
                    chance = random.random()
                    if chance < 0.7:
                        color, val, timer = (255, 0, 0), 1, 7000
                    elif chance < 0.9:
                        color, val, timer = (0, 100, 255), 3, 5000
                    else:
                        color, val, timer = (255, 215, 0), 5, 3000
                    
                    return {
                        "pos": pos, 
                        "color": color, 
                        "val": val, 
                        "timer": pygame.time.get_ticks() + timer # Тамақтың жоғалып кету уақыты
                    }
                
                if itype == "poison":
                    # Удың орнын қайтару
                    return {"pos": pos, "color": (138, 43, 226)}
                
                if itype == "pu":
                    # Кездейсоқ бонус түрін таңдау: жылдамдық, баяулату немесе қалқан
                    kind = random.choice(["speed", "slow", "shield"])
                    return {
                        "pos": pos, 
                        "kind": kind, 
                        "timer": pygame.time.get_ticks() + 8000 # Бонус 8 секунд тұрады
                    }

    def update(self):
        """Ойынның әр кадр сайынғы өзгерістері (Логика)"""
        now = pygame.time.get_ticks()

        # 1. Таймерлерді тексеру: тамақ немесе бонус ескірсе, жаңасын шығару
        if now > self.food["timer"]:
            self.food = self.spawn_item("normal")
        
        if self.powerup and now > self.powerup["timer"]:
            self.powerup = None
            self.pu_spawn_time = now + random.randint(5000, 10000)

        # Егер бонус жоқ болса және уақыты келсе — жаңа бонус шығару
        if not self.powerup and now > self.pu_spawn_time:
            self.powerup = self.spawn_item("pu")

        # Бонустың әсер ету уақыты бітсе, жылдамдықты қалпына келтіру
        if self.active_pu_end > 0 and now > self.active_pu_end:
            self.speed_mod = 0
            self.active_pu_end = 0

        # 2. Жыланның басын қозғалту
        head = self.snake[0].copy()
        if self.direction == "UP": head[1] -= BLOCK
        elif self.direction == "DOWN": head[1] += BLOCK
        elif self.direction == "LEFT": head[0] -= BLOCK
        elif self.direction == "RIGHT": head[0] += BLOCK

        # 3. Қақтығыстарды тексеру (Collision)
        if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= GAME_HEIGHT or 
            head in self.snake or head in self.obstacles):
            
            # Егер қалқан болса, жылан өлмейді, тек қалқан жоғалады
            if self.shield_active:
                self.shield_active = False
                return "MOVE" 
            
            # Қалқан болмаса — Ойын бітті, нәтижені базаға сақтау
            db.save_game_session(self.player_id, self.score, self.level)
            return "GAMEOVER"

        # Жыланның жаңа басын тізімнің басына қосу
        self.snake.insert(0, head)

        # 4. Бірдеңе жегенін тексеру
        # Кәдімгі тамақ жесе:
        if head == self.food["pos"]:
            self.score += self.food["val"]
            # Әр 5 ұпай сайын деңгейді көтеру және кедергілер қосу
            if self.score // 5 + 1 > self.level:
                self.level += 1
                self.generate_obstacles()
            self.food = self.spawn_item("normal")
            return "EAT"

        # У жеп қойса:
        elif head == self.poison["pos"]:
            if len(self.snake) > 2:
                self.snake.pop(); self.snake.pop() # Жылан 2 блокқа қысқарады
                self.poison = self.spawn_item("poison")
                return "POISON"
            else: 
                # Егер жылан тым қысқа болса және у жесе — өледі
                db.save_game_session(self.player_id, self.score, self.level)
                return "GAMEOVER"

        # Бонус (Power-up) жесе:
        elif self.powerup and head == self.powerup["pos"]:
            kind = self.powerup["kind"]
            if kind == "speed":
                self.speed_mod = 5 # Жылдамдықты арттыру
                self.active_pu_end = now + 5000 # 5 секундқа
            elif kind == "slow":
                self.speed_mod = -3 # Баяулату
                self.active_pu_end = now + 5000
            elif kind == "shield":
                self.shield_active = True # Қалқанды іске қосу
            
            self.powerup = None
            self.pu_spawn_time = now + random.randint(5000, 10000)
            return "POWERUP"

        else:
            # Егер ештеңе жемесе, жыланның құйрығын өшіру (қозғалыс эффектісі)
            self.snake.pop()

        return "MOVE"

    def generate_obstacles(self):
        """3-деңгейден бастап экранда кедергілер (тастар) пайда болады"""
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level + 2):
                while True:
                    x = random.randrange(0, WIDTH, BLOCK)
                    y = random.randrange(0, GAME_HEIGHT, BLOCK)
                    # Кедергі жыланның басына тым жақын түспеуі керек
                    dist = abs(x - self.snake[0][0]) + abs(y - self.snake[0][1])
                    if [x, y] not in self.snake and dist > BLOCK * 3:
                        self.obstacles.append([x, y])
                        break