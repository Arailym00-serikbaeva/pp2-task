import pygame
import sys

# Басқа файлдардан қажетті функцияларды импорттау
from persistence import load_settings, save_score # Баптауларды жүктеу және ұпай сақтау
from ui import (main_menu, settings_screen, leaderboard_screen, 
                game_over_screen, username_screen) # Интерфейс экрандары
from racer import run_game # Негізгі ойын процесі

def main():
    # Pygame модульдерін іске қосу
    pygame.init()
    pygame.mixer.init() # Дыбыс үшін

    # Экран өлшемдері мен тақырыбын орнату
    WIDTH, HEIGHT = 500, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Turbo Racer — TSIS3")
    clock = pygame.time.Clock() # FPS бақылау үшін

    # Бастапқы баптауларды жүктеу және ойыншы атын бос қалдыру
    settings    = load_settings()
    player_name = None

    # Ойынның негізгі циклі (Мәзір мен ойын арасында ауысу үшін)
    while True:
        # Бас мәзірді көрсету және қолданушының таңдауын алу
        choice = main_menu(screen, clock)

        # 1. Шығу таңдалса
        if choice == "quit":
            pygame.quit()
            sys.exit()

        # 2. Баптаулар таңдалса
        elif choice == "settings":
            settings = settings_screen(screen, clock)

        # 3. Рекордтар кестесі таңдалса
        elif choice == "leaderboard":
            leaderboard_screen(screen, clock)

        # 4. Ойынды бастау таңдалса
        elif choice == "play":
            # Егер ойыншы аты әлі енгізілмесе, ат сұрайтын экранды ашу
            if player_name is None:
                player_name = username_screen(screen, clock)

            # Ойынды қайталау циклі (Retry loop)
            while True: 
                # run_game функциясы ойынды бастайды және аяқталғанда нәтижелерді қайтарады
                score, distance, coins = run_game(
                    screen, clock, settings, player_name)

                # Нәтижені (ұпай мен қашықтықты) деректер қорына немесе файлға сақтау
                save_score(player_name, score, distance)

                # "Ойын бітті" экранын көрсету
                result = game_over_screen(
                    screen, clock, score, distance, coins, player_name)

                # Егер қолданушы "Қайталау" (retry) батырмасын басса
                if result == "retry":
                    continue # Ойынды сол атпен қайта бастау
                else:
                    # Егер мәзірге қайтса, келесі жолы жаңа ат сұрау үшін атын өшіру
                    player_name = None 
                    break

# Программаны іске қосу
if __name__ == "__main__":
    main()