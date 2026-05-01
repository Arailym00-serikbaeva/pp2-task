import pygame
import sys
import json
import random
import db  # Деректер қорымен жұмыс істейтін файлды импорттау
from game import Game, BLOCK, WIDTH, GAME_HEIGHT  # Ойын логикасын және өлшемдерді импорттау

# Pygame модульдерін іске қосу
pygame.init()
pygame.mixer.init() # Дыбыс үшін

# Экран өлшемдерін орнату (Ойын алаңы + төменгі ақпараттық панель үшін 50 пиксель)
SCREEN_HEIGHT = GAME_HEIGHT + 50
screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake PRO - Database Edition") # Терезе аты
clock = pygame.time.Clock() # Ойын жылдамдығын (FPS) бақылау үшін

# Әртүрлі өлшемдегі қаріптер (шрифт)
font_sm = pygame.font.SysFont("Arial", 22)
font_md = pygame.font.SysFont("Arial", 32)
font_lg = pygame.font.SysFont("Arial", 50)

# Баптауларды settings.json файлынан жүктеу функциясы
def load_settings():
    try:
        with open("settings.json", "r") as f: return json.load(f)
    except: 
        # Егер файл болмаса, стандартты баптауларды қайтару
        return {"snake_color": [0, 200, 0], "grid_overlay": True, "sound": True}

conf = load_settings() # Баптауларды айнымалыға сақтау

# Баптауларды файлға сақтау функциясы
def save_settings(s):
    with open("settings.json", "w") as f: json.dump(s, f)

# Экранға мәтін шығаруға арналған көмекші функция
def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center: rect.center = (x, y) # Ортаға бағыттау
    else: rect.topleft = (x, y)
    screen.blit(img, rect)

# Батырмалар (кнопка) жасауға арналған класс
class Button:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color # Негізгі түсі
        self.hover_color = hover_color # Тышқан үстіне келгендегі түсі
        self.is_hovered = False

    def draw(self, surface):
        # Тышқан батырма үстінде тұрса, түсін өзгерту
        curr = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, curr, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10) # Жиектеме
        draw_text(self.text, font_sm, (255, 255, 255), self.rect.centerx, self.rect.centery, True)

    def check_hover(self, pos):
        # Тышқан курсоры батырманың үстінде ме, жоқ па тексеру
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos, up):
        # Батырма басылды ма тексеру
        return self.is_hovered and up

# Рекордтар кестесі экраны
def leaderboard_screen():
    btn_back = Button("BACK", WIDTH//2 - 60, 500, 120, 40, (50, 50, 50), (80, 80, 80))
    while True:
        m_pos = pygame.mouse.get_pos(); m_up = False
        screen.fill((10, 10, 15)) # Фон түсі
        draw_text("TOP 10 PLAYERS", font_md, (255, 215, 0), WIDTH//2, 50, True)
        
        # Деректер қорынан үздік 10 ойыншыны алу
        data = db.get_top_10()
        for i, row in enumerate(data):
            draw_text(f"{i+1}. {row[0]} - {row[1]} pts", font_sm, (255, 255, 255), 100, 120 + i*30)

        btn_back.check_hover(m_pos); btn_back.draw(screen)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONUP: m_up = True
        
        if btn_back.is_clicked(m_pos, m_up): return # Артқа қайту
        pygame.display.flip()
        clock.tick(60)

# Бас мәзір (Main Menu)
def main_menu():
    username = "" # Ойыншы аты
    btn_play = Button("PLAY", WIDTH//2 - 100, 300, 200, 50, (0, 120, 0), (0, 180, 0))
    btn_leader = Button("LEADERBOARD", WIDTH//2 - 100, 370, 200, 50, (0, 80, 150), (0, 120, 200))
    btn_quit = Button("QUIT", WIDTH//2 - 100, 440, 200, 50, (120, 0, 0), (180, 0, 0))

    while True:
        m_pos = pygame.mouse.get_pos(); m_up = False
        screen.fill((20, 25, 30))
        draw_text("SNAKE PRO", font_lg, (255, 215, 0), WIDTH//2, 100, True)
        
        # Ойыншы атын жазатын өріс (Input box)
        pygame.draw.rect(screen, (40, 45, 50), (WIDTH//2 - 150, 180, 300, 50), border_radius=5)
        draw_text(f"User: {username}|", font_md, (255, 255, 255), WIDTH//2, 205, True)

        for b in [btn_play, btn_leader, btn_quit]:
            b.check_hover(m_pos); b.draw(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONUP: m_up = True
            if e.type == pygame.KEYDOWN:
                # Артқа өшіру (Backspace)
                if e.key == pygame.K_BACKSPACE: username = username[:-1]
                # Жаңа әріп қосу (макс. 12 символ)
                elif len(username) < 12 and e.unicode.isprintable(): username += e.unicode

        # PLAY басылғанда аты бос болмаса, ойынды бастау
        if btn_play.is_clicked(m_pos, m_up) and username.strip(): return username.strip()
        if btn_leader.is_clicked(m_pos, m_up): leaderboard_screen()
        if btn_quit.is_clicked(m_pos, m_up): pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Негізгі ойын процесі
def play_game(user):
    game = Game(user, conf) # Ойын объектісін жасау
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            # Пернетақта арқылы бағытты басқару
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and game.direction != "DOWN": game.direction = "UP"
                if e.key == pygame.K_DOWN and game.direction != "UP": game.direction = "DOWN"
                if e.key == pygame.K_LEFT and game.direction != "RIGHT": game.direction = "LEFT"
                if e.key == pygame.K_RIGHT and game.direction != "LEFT": game.direction = "RIGHT"

        # Ойын күйін жаңарту (жыланның жүруі, тамақ жеуі)
        status = game.update()
        if status == "GAMEOVER":
            # Ойын бітсе, нәтижені деректер қорына сақтау
            db.save_game_session(game.player_id, game.score, game.level)
            return # Мәзірге қайту

        screen.fill((15, 15, 20)) # Ойын алаңын тазарту
        
        # Жыланды сызу
        for i, seg in enumerate(game.snake):
            pygame.draw.rect(screen, conf["snake_color"], (*seg, BLOCK, BLOCK), border_radius=5)
        
        # Тамақты сызу
        pygame.draw.rect(screen, (255, 0, 0), (*game.food["pos"], BLOCK, BLOCK), border_radius=10)

        # Статистика панелін сызу (Ұпай, Деңгей, Жеке рекорд)
        pygame.draw.rect(screen, (30, 30, 40), (0, GAME_HEIGHT, WIDTH, 50))
        draw_text(f"Score: {game.score}  Level: {game.level}  PB: {game.pb}", font_sm, (255, 255, 255), 20, GAME_HEIGHT + 12)

        pygame.display.flip() # Экранды жаңарту
        # Жылдамдық деңгейге байланысты артып отырады
        clock.tick(game.base_speed + game.level)

# Программаның басталу нүктесі
if __name__ == "__main__":
    db.init_db() # Деректер қорын іске қосу (кестелер жасау)
    while True:
        u = main_menu() # Алдымен мәзірді көрсету
        play_game(u) # Сосын ойынды бастау