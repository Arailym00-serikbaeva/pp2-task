import pygame
import sys
from persistence import load_leaderboard, save_settings, load_settings

# ─── Түстер палитрасы (Алтын түсті стиль) ──────────────────────────────────────
GOLD_BASE   = (218, 165, 32)
GOLD_LIGHT  = (255, 223, 0)
GOLD_DARK   = (101, 67, 33)
VOID_BLUE   = (10, 12, 20)
WHITE       = (250, 250, 245)
BLACK       = (0, 0, 0)
GRAY        = (100, 100, 100)
CYAN        = (0, 220, 255)

# Көлік түстерінің нұсқалары
CAR_COLOR_OPTIONS = {
    "Blue":   [  0, 150, 255],
    "Red":    [255,  50,  50],
    "Green":  [ 50, 220,  80],
    "Yellow": [255, 220,   0],
    "Purple": [160,  80, 240],
    "White":  [255, 255, 255],
}
CAR_TYPES = ["Taxi", "Sport", "Truck"]
DIFFICULTIES = ["Easy", "Normal", "Hard"]

def draw_bg(screen):
    """Экранның фонын қара-көк түспен толтыру"""
    screen.fill(VOID_BLUE)

def draw_button(screen, rect, text, font, is_hovered=False, active=False):
    """Әдемі батырмаларды (көлеңкесімен және жиегімен) салу функциясы"""
    # Түсін анықтау: тышқан үстіне келгенде немесе батырма белсенді болғанда өзгереді
    color = GOLD_BASE if is_hovered else (30, 35, 50)
    if active: color = GOLD_LIGHT
    
    # Батырманың көлеңкесі
    shadow_rect = rect.move(3, 3)
    pygame.draw.rect(screen, (0, 0, 0, 150), shadow_rect, border_radius=10)
    
    # Батырманың негізгі денесі және жиегі
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, GOLD_LIGHT, rect, 2, border_radius=10)
    
    # Батырма ішіндегі мәтін
    txt_col = BLACK if is_hovered or active else WHITE
    txt = font.render(text, True, txt_col)
    screen.blit(txt, txt.get_rect(center=rect.center))

def main_menu(screen, clock):
    """Бас мәзір: Ойнау, Баптаулар, Рекордтар және Шығу"""
    font_big = pygame.font.SysFont("consolas", 50, bold=True)
    font_med = pygame.font.SysFont("consolas", 28)
    btns = {
        "play": pygame.Rect(150, 250, 200, 60),
        "settings": pygame.Rect(150, 330, 200, 60),
        "leaderboard": pygame.Rect(150, 410, 200, 60),
        "quit": pygame.Rect(150, 490, 200, 60)
    }
    while True:
        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for res, rect in btns.items():
                    if rect.collidepoint(m_pos): return res
        
        draw_bg(screen)
        txt = font_big.render("GOLDEN RACER", True, GOLD_LIGHT)
        screen.blit(txt, txt.get_rect(center=(250, 120)))
        
        for res, rect in btns.items():
            draw_button(screen, rect, res.upper(), font_med, rect.collidepoint(m_pos))
        
        pygame.display.flip()
        clock.tick(60)

def settings_screen(screen, clock):
    """Гараж баптаулары: көлік моделін, қиындықты және түсті таңдау"""
    settings = load_settings()
    if "difficulty" not in settings: settings["difficulty"] = "Normal"
    
    font_med = pygame.font.SysFont("consolas", 24)
    font_sm  = pygame.font.SysFont("consolas", 18)
    btn_back = pygame.Rect(150, 630, 200, 45)

    while True:
        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(m_pos):
                    save_settings(settings); return settings
                
                # Көлік түрін таңдау логикасы
                for i, c_type in enumerate(CAR_TYPES):
                    if pygame.Rect(50 + i*150, 160, 130, 40).collidepoint(m_pos):
                        settings["car_type"] = c_type
                
                # Қиындықты таңдау логикасы
                for i, diff_name in enumerate(DIFFICULTIES):
                    if pygame.Rect(50 + i*150, 280, 130, 40).collidepoint(m_pos):
                        settings["difficulty"] = diff_name

                # Түсті таңдау логикасы
                for i, (name, col) in enumerate(CAR_COLOR_OPTIONS.items()):
                    rect = pygame.Rect(100 + (i%2)*160, 410 + (i//2)*45, 140, 35)
                    if rect.collidepoint(m_pos):
                        settings["car_color"] = col
        
        draw_bg(screen)
        title = font_med.render("GARAGE SETTINGS", True, GOLD_LIGHT)
        screen.blit(title, title.get_rect(center=(250, 50)))
        
        # Экранға баптау бөлімдерін шығару (Model, Difficulty, Paint)
        screen.blit(font_sm.render("SELECT MODEL:", True, WHITE), (50, 130))
        for i, c_type in enumerate(CAR_TYPES):
            rect = pygame.Rect(50 + i*150, 160, 130, 40)
            draw_button(screen, rect, c_type, font_sm, rect.collidepoint(m_pos), settings.get("car_type") == c_type)
            
        screen.blit(font_sm.render("DIFFICULTY LEVEL:", True, WHITE), (50, 250))
        for i, diff_name in enumerate(DIFFICULTIES):
            rect = pygame.Rect(50 + i*150, 280, 130, 40)
            draw_button(screen, rect, diff_name.upper(), font_sm, rect.collidepoint(m_pos), settings.get("difficulty") == diff_name)

        screen.blit(font_sm.render("BODY PAINT:", True, WHITE), (50, 380))
        for i, (name, col_val) in enumerate(CAR_COLOR_OPTIONS.items()):
            rect = pygame.Rect(100 + (i%2)*160, 410 + (i//2)*45, 140, 35)
            pygame.draw.rect(screen, col_val, rect, border_radius=4)
            border_col = GOLD_LIGHT if settings.get("car_color") == col_val else GRAY
            pygame.draw.rect(screen, border_col, rect, 2, border_radius=4)
            
            txt = font_sm.render(name, True, BLACK if sum(col_val) > 400 else WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))

        draw_button(screen, btn_back, "SAVE & EXIT", font_sm, btn_back.collidepoint(m_pos))
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(screen, clock, score, distance, coins, player_name):
    """Ойын аяқталғандағы экран: нәтижелерді көрсету"""
    font_big = pygame.font.SysFont("consolas", 48, bold=True)
    font_sm = pygame.font.SysFont("consolas", 22)
    btn_retry = pygame.Rect(50, 550, 180, 50)
    btn_menu = pygame.Rect(270, 550, 180, 50)
    while True:
        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(m_pos): return "retry"
                if btn_menu.collidepoint(m_pos): return "menu"
        
        draw_bg(screen)
        title = font_big.render("RACE FINISHED", True, GOLD_LIGHT)
        screen.blit(title, title.get_rect(center=(250, 200)))
        
        res = font_sm.render(f"Driver: {player_name} | Score: {score}", True, WHITE)
        screen.blit(res, res.get_rect(center=(250, 300)))
        
        draw_button(screen, btn_retry, "RETRY", font_sm, btn_retry.collidepoint(m_pos))
        draw_button(screen, btn_menu, "MENU", font_sm, btn_menu.collidepoint(m_pos))
        
        pygame.display.flip()
        clock.tick(60)

def username_screen(screen, clock):
    """Ойыншының атын енгізу экраны"""
    font_med = pygame.font.SysFont("consolas", 28)
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name: return name
                elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                else: 
                    if len(name) < 12: name += event.unicode
        
        draw_bg(screen)
        title = font_med.render("ENTER PILOT NAME:", True, GOLD_LIGHT)
        screen.blit(title, title.get_rect(center=(250, 300)))
        
        # Енгізіліп жатқан атты көрсету
        txt = font_med.render(name + "_", True, GOLD_BASE)
        screen.blit(txt, txt.get_rect(center=(250, 360)))
        
        pygame.display.flip()
        clock.tick(60)

def leaderboard_screen(screen, clock):
    """Ең үздік 10 ойыншының тізімін көрсету"""
    font_med = pygame.font.SysFont("consolas", 28)
    font_sm  = pygame.font.SysFont("consolas", 20)
    btn_back = pygame.Rect(150, 600, 200, 50)
    while True:
        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and btn_back.collidepoint(m_pos): return
            
        draw_bg(screen)
        title = font_med.render("TOP DRIVERS", True, GOLD_LIGHT)
        screen.blit(title, title.get_rect(center=(250, 80)))
        
        # Рекордтарды жүктеп, тізіммен шығару
        lb = load_leaderboard()
        for i, entry in enumerate(lb[:10]):
            txt = font_sm.render(f"{i+1}. {entry['name']} - {entry['score']} pts", True, WHITE)
            screen.blit(txt, (100, 150 + i*40))
            
        draw_button(screen, btn_back, "BACK", font_sm, btn_back.collidepoint(m_pos))
        pygame.display.flip()
        clock.tick(60)