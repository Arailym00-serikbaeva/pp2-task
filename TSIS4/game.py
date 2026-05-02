import pygame
import random
import db  # Деректер қорымен жұмыс істейтін файл

BLOCK = 20        
WIDTH = 600       
GAME_HEIGHT = 600 

class Game:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings
        # Деректер қорынан ойыншының ID-ін және ең жақсы нәтижесін (Personal Best) алу
        self.player_id = db.get_or_create_player(username)
        self.pb = db.get_personal_best(self.player_id)
        self.reset() # Ойынды бастапқы күйге келтіру

    def reset(self):
        # Жыланның бастапқы денесі (3 блок)
        self.snake = [[300, 300], [280, 300], [260, 300]]
        self.direction = "RIGHT" # Бастапқы бағыты
        self.score = 0           # Ұпай
        self.level = 1           # Деңгей
        self.base_speed = 7      # Негізгі жылдамдық
        self.speed_mod = 0       # Бонустардан келетін жылдамдық өзгерісі
        self.obstacles = []      # Кедергілер тізімі
        self.food = self.spawn_item("normal")  # Кәдімгі тамақ шығару
        self.poison = self.spawn_item("poison") # У шығару
        self.powerup = None      # Белсенді бонус (басында жоқ)
        
        # Келесі бонус 5-10 секунд аралығында шығуы үшін таймер қою
        self.pu_spawn_time = pygame.time.get_ticks() + random.randint(5000, 10000)
        self.active_pu_end = 0   # Бонус әсерінің аяқталу уақыты
        self.shield_active = False # Қалқан белсенділігі

    # Ойын алаңында заттарды (тамақ, у, бонус) кездейсоқ шығару функциясы
    def spawn_item(self, itype):
        while True:
            x = random.randrange(0, WIDTH, BLOCK)
            y = random.randrange(0, GAME_HEIGHT, BLOCK)
            pos = [x, y]
            
            # Егер шыққан орын жыланның үсті немесе кедергі болмаса ғана қабылдау
            if pos not in self.snake and pos not in self.obstacles:
                if itype == "normal":
                    chance = random.random()
                    # Түрлі тамақтардың пайда болу ықтималдығы мен ұпайы
                    if chance < 0.7:
                        color, val, timer = (255, 0, 0), 1, 7000   # Қызыл (қарапайым)
                    elif chance < 0.9:
                        color, val, timer = (0, 100, 255), 3, 5000 # Көк (сирек)
                    else:
                        color, val, timer = (255, 215, 0), 5, 3000 # Алтын (өте сирек)
                    
                    return {
                        "pos": pos, 
                        "color": color, 
                        "val": val, 
                        "timer": pygame.time.get_ticks() + timer # Тамақтың жоғалып кету уақыты
                    }
                
                if itype == "poison":
                    return {"pos": pos, "color": (138, 43, 226)} # Күлгін түсті у
                
                if itype == "pu":
                    # Бонустардың түрі: жылдамдық, баяулату, қалқан
                    kind = random.choice(["speed", "slow", "shield"])
                    return {
                        "pos": pos, 
                        "kind": kind, 
                        "timer": pygame.time.get_ticks() + 8000 # 8 секундтан кейін жоғалады
                    }

    def update(self):
        now = pygame.time.get_ticks()

        # 1. Таймерлерді тексеру (тамақ пен бонустардың уақыты бітті ме)
        if now > self.food["timer"]:
            self.food = self.spawn_item("normal")
        
        if self.powerup and now > self.powerup["timer"]:
            self.powerup = None
            self.pu_spawn_time = now + random.randint(5000, 10000)

        # Жаңа бонус шығаратын уақыт келді ме
        if not self.powerup and now > self.pu_spawn_time:
            self.powerup = self.spawn_item("pu")

        # Бонус әсерінің (жылдамдық/баяулық) уақытын тексеру
        if self.active_pu_end > 0 and now > self.active_pu_end:
            self.speed_mod = 0
            self.active_pu_end = 0

        # 2. Жыланның қозғалысы (басын жаңа блокқа жылжыту)
        head = self.snake[0].copy()
        if self.direction == "UP": head[1] -= BLOCK
        elif self.direction == "DOWN": head[1] += BLOCK
        elif self.direction == "LEFT": head[0] -= BLOCK
        elif self.direction == "RIGHT": head[0] += BLOCK

        # 3. Қақтығыстарды (коллизия) тексеру
        # Шетке тию, өзіне тию немесе кедергіге тию
        if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= GAME_HEIGHT or 
            head in self.snake or head in self.obstacles):
            
            # Егер қалқан белсенді болса, өлмейді, тек қалқаны өшеді
            if self.shield_active:
                self.shield_active = False
                return "MOVE" 
            
            # Ойын аяқталса, нәтижені ДҚ-ға сақтау
            db.save_game_session(self.player_id, self.score, self.level)
            return "GAMEOVER"

        self.snake.insert(0, head) # Жаңа басты қосу

        # 4. Нәрселерді жеуді тексеру
        # Тамақ жесе
        if head == self.food["pos"]:
            self.score += self.food["val"]
            # Әр 5 ұпай сайын деңгейді көтеру және кедергілер қосу
            if self.score // 5 + 1 > self.level:
                self.level += 1
                self.generate_obstacles()
            self.food = self.spawn_item("normal")
            return "EAT"

        # У жесе (жылан қысқарады)
        elif head == self.poison["pos"]:
            if len(self.snake) > 2:
                self.snake.pop(); self.snake.pop() # Екі блокқа қысқарту
                self.poison = self.spawn_item("poison")
                return "POISON"
            else: 
                db.save_game_session(self.player_id, self.score, self.level)
                return "GAMEOVER"

        # Бонус жесе
        elif self.powerup and head == self.powerup["pos"]:
            kind = self.powerup["kind"]
            if kind == "speed":
                self.speed_mod = 5
                self.active_pu_end = now + 5000 # 5 секундқа жылдамдайды
            elif kind == "slow":
                self.speed_mod = -3
                self.active_pu_end = now + 5000 # 5 секундқа баяулайды
            elif kind == "shield":
                self.shield_active = True
            
            self.powerup = None
            self.pu_spawn_time = now + random.randint(5000, 10000)
            return "POWERUP"

        else:
            self.snake.pop() # Ештеңе жемесе, құйрығын алып тастау (қозғалыс эффектісі)

        return "MOVE"

    # Кедергілерді (қабырғаларды) жасау функциясы
    def generate_obstacles(self):
        self.obstacles = []
        if self.level >= 3: # Кедергілер тек 3-деңгейден бастап пайда болады
            for _ in range(self.level + 2):
                while True:
                    x = random.randrange(0, WIDTH, BLOCK)
                    y = random.randrange(0, GAME_HEIGHT, BLOCK)
                    # Жыланның басынан кемінде 3 блок қашықтықта жасау (тұйыққа тірелмеу үшін)
                    dist = abs(x - self.snake[0][0]) + abs(y - self.snake[0][1])
                    if [x, y] not in self.snake and dist > BLOCK * 3:
                        self.obstacles.append([x, y])
                        break