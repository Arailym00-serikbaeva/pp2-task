import pygame
import sys
import json
import random
import db # Деректер қорымен жұмыс (database)
from game import Game, BLOCK, WIDTH, GAME_HEIGHT # Ойын логикасын импорттау

pygame.init()
pygame.mixer.init() # Дыбыстармен жұмыс істеуді іске қосу

SCREEN_HEIGHT = GAME_HEIGHT + 50 # Астыңғы жақтағы статистика (ұпай) үшін қосымша 50 пиксель
screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake PRO - Database Edition")
clock = pygame.time.Clock()

# Шрифтер (әр түрлі өлшемдегі мәтіндер үшін)
font_sm = pygame.font.SysFont("Arial", 22)
font_md = pygame.font.SysFont("Arial", 32)
font_lg = pygame.font.SysFont("Arial", 50)

# --- ДЫБЫС ЛОГИКАСЫ ---
try:
    click_sound = pygame.mixer.Sound("assets/click.wav") #(клик) дыбысын жүктеу
except:
    click_sound = None
    print("Предупреждение: assets/click.wav не найден")

def play_click():
    # Егер баптауларда дыбыс қосулы болса, клик дыбысын ойнату
    if conf.get("sound", True) and click_sound:
        click_sound.play()

# --- ТҮЙМЕ (BUTTON) КЛАССЫ ---
class Button:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color             # Негізгі түсі
        self.hover_color = hover_color # Тышқан үстіне келгендегі түсі
        self.is_hovered = False

    def draw(self, surface):
        # Тышқан үстінде тұрса hover_color, тұрмаса негізгі түспен салу
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10) # Жиегі
        
        txt_img = font_sm.render(self.text, True, (255, 255, 255))
        txt_rect = txt_img.get_rect(center=self.rect.center)
        surface.blit(txt_img, txt_rect)

    def check_hover(self, mouse_pos):
        # Тышқанның түйме үстінде тұрғанын тексеру
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_up):
        # Тышқанмен түймені басқанын тексеру
        return self.is_hovered and mouse_up

# --- БАПТАУЛАРДЫ ЖҮКТЕУ ЖӘНЕ САҚТАУ ---
def load_settings():
    try:
        with open("settings.json", "r") as f: return json.load(f)
    except: return {"snake_color": [0, 200, 0], "grid_overlay": True, "sound": True}

conf = load_settings()

def save_settings(s):
    with open("settings.json", "w") as f: json.dump(s, f)

# Мәтінді экранға шығаруға арналған көмекші функция
def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center: rect.center = (x, y)
    else: rect.topleft = (x, y)
    screen.blit(img, rect)

# --- ЭКРАНДАР (МӘЗІРЛЕР) ---

# Лидерлер кестесі экраны
def leaderboard_screen():
    btn_back = Button("BACK", WIDTH//2 - 60, 550, 120, 40, (50, 50, 50), (80, 80, 80))
    while True:
        mouse_pos = pygame.mouse.get_pos(); mouse_up = False
        screen.fill((10, 10, 15))
        draw_text("TOP 10 PLAYERS", font_md, (255, 215, 0), WIDTH//2, 50, True)
        
        # Деректер қорынан үздік 10 ойыншыны алып, экранға шығару
        top_players = db.get_top_10()
        for i, (name, score, lvl, date) in enumerate(top_players):
            txt = f"{i+1}. {name[:10]} - {score} pts (Lvl {lvl})"
            draw_text(txt, font_sm, (255, 255, 255), 150, 120 + i*35)

        btn_back.check_hover(mouse_pos); btn_back.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONUP: mouse_up = True
        
        if btn_back.is_clicked(mouse_pos, mouse_up):
            play_click(); return
        pygame.display.flip()
        clock.tick(60)

# Баптаулар экраны
def settings_screen():
    global conf
    btn_grid = Button("TOGGLE GRID", WIDTH//2 - 100, 200, 200, 40, (70, 70, 70), (100, 100, 100))
    btn_sound = Button("SOUND: ON" if conf["sound"] else "SOUND: OFF", WIDTH//2 - 100, 260, 200, 40, (70, 70, 70), (100, 100, 100))
    btn_color = Button("RANDOM COLOR", WIDTH//2 - 100, 320, 200, 40, (70, 70, 70), (100, 100, 100))
    btn_save = Button("SAVE & EXIT", WIDTH//2 - 100, 450, 200, 50, (0, 120, 0), (0, 180, 0))

    while True:
        mouse_pos = pygame.mouse.get_pos(); mouse_up = False
        screen.fill((30, 35, 40))
        draw_text("SETTINGS", font_md, (255, 255, 255), WIDTH//2, 50, True)
        
        grid_status = "ON" if conf["grid_overlay"] else "OFF"
        draw_text(f"Grid: {grid_status}", font_sm, (200, 200, 200), WIDTH//2, 170, True)
        # Жыланның таңдалған түсін кішкене шаршы қылып көрсету
        pygame.draw.rect(screen, conf["snake_color"], (WIDTH//2 - 20, 370, 40, 40), border_radius=5)

        for b in [btn_grid, btn_sound, btn_color, btn_save]:
            b.check_hover(mouse_pos); b.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONUP: mouse_up = True

        if btn_grid.is_clicked(mouse_pos, mouse_up):
            play_click(); conf["grid_overlay"] = not conf["grid_overlay"] # Торды қосу/өшіру
        if btn_sound.is_clicked(mouse_pos, mouse_up):
            conf["sound"] = not conf["sound"] # Дыбысты қосу/өшіру
            btn_sound.text = "SOUND: ON" if conf["sound"] else "SOUND: OFF"
            play_click()
        if btn_color.is_clicked(mouse_pos, mouse_up):
            play_click(); conf["snake_color"] = [random.randint(50,255) for _ in range(3)] # Жылан түсін кездейсоқ өзгерту
        if btn_save.is_clicked(mouse_pos, mouse_up):
            play_click(); save_settings(conf); return # Сақтау және шығу
        
        pygame.display.flip()
        clock.tick(60)

# Ойын біткен кездегі экран
def game_over_screen(game):
    btn_retry = Button("RETRY", WIDTH//2 - 110, 450, 100, 45, (0, 100, 0), (0, 150, 0))
    btn_menu = Button("MENU", WIDTH//2 + 10, 450, 100, 45, (100, 100, 100), (150, 150, 150))
    while True:
        mouse_pos = pygame.mouse.get_pos(); mouse_up = False
        screen.fill((50, 10, 10)) # Қызыл реңкті фон
        draw_text("GAME OVER", font_lg, (255, 255, 255), WIDTH//2, 150, True)
        draw_text(f"Score: {game.score}", font_md, (255, 255, 255), WIDTH//2, 230, True)
        draw_text(f"Level: {game.level}", font_sm, (200, 200, 200), WIDTH//2, 280, True)
        draw_text(f"Personal Best: {game.pb}", font_sm, (255, 215, 0), WIDTH//2, 330, True)
        
        for b in [btn_retry, btn_menu]: b.check_hover(mouse_pos); b.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONUP: mouse_up = True
        
        if btn_retry.is_clicked(mouse_pos, mouse_up): play_click(); return "RETRY"
        if btn_menu.is_clicked(mouse_pos, mouse_up): play_click(); return "MENU"
        pygame.display.flip()
        clock.tick(60)

# Негізгі мәзір (Аты-жөнін жазу және бастау)
def main_menu():
    username = ""
    btn_play = Button("PLAY", WIDTH//2 - 100, 320, 200, 50, (0, 150, 0), (0, 200, 0))
    btn_leader = Button("LEADERBOARD", WIDTH//2 - 100, 380, 200, 50, (0, 100, 150), (0, 150, 250))
    btn_settings = Button("SETTINGS", WIDTH//2 - 100, 440, 200, 50, (100, 100, 100), (150, 150, 150))
    btn_quit = Button("QUIT", WIDTH//2 - 100, 500, 200, 50, (150, 0, 0), (200, 0, 0))
    
    buttons = [btn_play, btn_leader, btn_settings, btn_quit]

    while True:
        mouse_pos = pygame.mouse.get_pos(); mouse_up = False
        screen.fill((20, 25, 30))
        draw_text("SNAKE PRO", font_lg, (255, 215, 0), WIDTH//2, 100, True)
        
        # Аты-жөнін жазатын жолақ (Input box)
        pygame.draw.rect(screen, (40, 45, 50), (WIDTH//2 - 150, 200, 300, 50), border_radius=5)
        draw_text(f"User: {username}|", font_md, (255, 255, 255), WIDTH//2, 225, True)

        for btn in buttons:
            btn.check_hover(mouse_pos); btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONUP: mouse_up = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip(): # ENTER басса
                    play_click(); return username
                elif event.key == pygame.K_BACKSPACE: username = username[:-1] # Өшіру
                else:
                    # Тек басып шығарылатын таңбаларды және максимум 12 әріп алу
                    if len(username) < 12 and event.unicode.isprintable():
                        username += event.unicode

        if btn_play.is_clicked(mouse_pos, mouse_up) and username.strip():
            play_click(); return username
        if btn_leader.is_clicked(mouse_pos, mouse_up):
            play_click(); leaderboard_screen()
        if btn_settings.is_clicked(mouse_pos, mouse_up):
            play_click(); settings_screen()
        if btn_quit.is_clicked(mouse_pos, mouse_up):
            play_click(); pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Ойын процесін жүргізу функциясы
def play_game(username):
    game = Game(username, conf)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            # Басқару түймелері
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != "DOWN": game.direction = "UP"
                if event.key == pygame.K_DOWN and game.direction != "UP": game.direction = "DOWN"
                if event.key == pygame.K_LEFT and game.direction != "RIGHT": game.direction = "LEFT"
                if event.key == pygame.K_RIGHT and game.direction != "LEFT": game.direction = "RIGHT"

        status = game.update()
        if status == "GAMEOVER":
            if game_over_screen(game) == "RETRY": 
                game.reset() # Қайта бастау
                continue
            else: return # Мәзірге қайту
        elif status in ["EAT", "POISON", "POWERUP"]:
            play_click() # Маңызды әрекеттер кезінде дыбыс шығару

        screen.fill((15, 15, 20))

        # Фондағы торды салу (егер қосулы болса)
        if conf["grid_overlay"]:
            for x in range(0, WIDTH, BLOCK): pygame.draw.line(screen, (25,25,30), (x,0), (x, GAME_HEIGHT))
            for y in range(0, GAME_HEIGHT, BLOCK): pygame.draw.line(screen, (25,25,30), (0,y), (WIDTH, y))

        # Кедергілерді салу
        for obs in game.obstacles:
            pygame.draw.rect(screen, (255, 100, 0), (*obs, BLOCK, BLOCK), border_radius=5)

        # Бонустарды (Power-up) салу (шеңбер түрінде)
        if game.powerup:
            p_pos = game.powerup["pos"]
            p_color = (255, 255, 0) if game.powerup["kind"] == "speed" else (0, 255, 255)
            pygame.draw.circle(screen, p_color, (p_pos[0] + BLOCK//2, p_pos[1] + BLOCK//2), 8)

        # Тамақты салу
        food_pos = game.food["pos"]
        pygame.draw.rect(screen, game.food["color"], (*food_pos, BLOCK, BLOCK), border_radius=8)
        
        # Уды салу (ішінде крест "X" белгісі бар)
        poison_pos = game.poison["pos"]
        pygame.draw.rect(screen, game.poison["color"], (*poison_pos, BLOCK, BLOCK), border_radius=5)
        pygame.draw.line(screen, (255, 255, 255), (poison_pos[0]+5, poison_pos[1]+5), (poison_pos[0]+15, poison_pos[1]+15), 2)
        pygame.draw.line(screen, (255, 255, 255), (poison_pos[0]+15, poison_pos[1]+5), (poison_pos[0]+5, poison_pos[1]+15), 2)

        # --- ЖЫЛАНДЫ СУРЕТТЕУ ---
        for i, seg in enumerate(game.snake):
            main_col = list(conf["snake_color"])
            # Жыланның құйрығына қарай түсін біртіндеп күңгірттеу (gradient эффектісі)
            factor = max(0.3, 1 - (i / len(game.snake)))
            color = [int(c * factor) for c in main_col]
            
            if i == 0: # БАСЫ
                pygame.draw.rect(screen, color, (*seg, BLOCK, BLOCK), border_radius=8)
                
                # Көздерін салу
                eye_color = (0, 0, 0); eye_size = 4
                # Қай жаққа қарап тұрғанына байланысты көздерінің орнын өзгерту
                if game.direction == "RIGHT":
                    pygame.draw.circle(screen, eye_color, (seg[0] + 14, seg[1] + 6), eye_size)
                    pygame.draw.circle(screen, eye_color, (seg[0] + 14, seg[1] + 14), eye_size)
                elif game.direction == "LEFT":
                    pygame.draw.circle(screen, eye_color, (seg[0] + 6, seg[1] + 6), eye_size)
                    pygame.draw.circle(screen, eye_color, (seg[0] + 6, seg[1] + 14), eye_size)
                elif game.direction == "UP":
                    pygame.draw.circle(screen, eye_color, (seg[0] + 6, seg[1] + 6), eye_size)
                    pygame.draw.circle(screen, eye_color, (seg[0] + 14, seg[1] + 6), eye_size)
                elif game.direction == "DOWN":
                    pygame.draw.circle(screen, eye_color, (seg[0] + 6, seg[1] + 14), eye_size)
                    pygame.draw.circle(screen, eye_color, (seg[0] + 14, seg[1] + 14), eye_size)

                # Егер қалқан (shield) белсенді болса, айналасында ақ жиек болады
                if game.shield_active:
                    pygame.draw.rect(screen, (255, 255, 255), (*seg, BLOCK, BLOCK), 2, border_radius=10)
            else: # ДЕНЕСІ
                pygame.draw.rect(screen, color, (seg[0]+1, seg[1]+1, BLOCK-2, BLOCK-2), border_radius=5)

        # Төменгі статистикалық панель (Score, Level, Best)
        pygame.draw.rect(screen, (30, 30, 40), (0, GAME_HEIGHT, WIDTH, 50))
        draw_text(f"Score: {game.score}", font_sm, (255, 255, 255), 20, GAME_HEIGHT + 12)
        draw_text(f"Level: {game.level}", font_sm, (0, 255, 0), WIDTH//2 - 40, GAME_HEIGHT + 12)
        draw_text(f"Best: {game.pb}", font_sm, (255, 215, 0), WIDTH - 120, GAME_HEIGHT + 12)

        pygame.display.flip()
        # Ойын жылдамдығы: негізгі + деңгей + бонустық жылдамдық
        clock.tick(game.base_speed + game.level + game.speed_mod)

# Ойынның басталу нүктесі
if __name__ == "__main__":
    while True:
        user = main_menu() # 1. Мәзірді көрсету және атты алу
        play_game(user)    # 2. Ойынды бастау