import pygame
import sys

# Pygame модульдерін іске қосу
pygame.init()

# Экран өлшемдерін орнату
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Сурет салу бағдарламасы")

# Кадр жиілігін бақылау үшін таймер
clock = pygame.time.Clock()

# Түстерді анықтау (RGB форматында)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Түстер тізімі және таңдалған бастапқы түс
colors = [BLACK, RED, GREEN, BLUE]
current_color = BLACK

# Бастапқы режим - еркін сурет салу
mode = "draw"

# Тышқанның күйін және позицияларын сақтайтын айнымалылар
drawing = False      # Сурет салынып жатыр ма?
start_pos = None     # Фигураның басталатын нүктесі
last_pos = None      # Соңғы нүкте (еркін сызу үшін)

# Мәтін жазу үшін қаріп (шрифт)
font = pygame.font.SysFont(None, 24)

# Экранды ақ түспен толтыру
screen.fill(WHITE)

while True:
    # Барлық оқиғаларды (events) тексеру
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Тышқан батырмасы басылғанда
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            mx, my = event.pos

            # 1. Түсті таңдау (жоғарғы сол жақ бұрыштағы квадраттарды басу)
            for i, c in enumerate(colors):
                if pygame.Rect(10 + i*50, 10, 40, 40).collidepoint(mx, my):
                    current_color = c

            # 2. Негізгі режимдерді таңдау батырмалары
            if pygame.Rect(250, 10, 80, 40).collidepoint(mx, my):
                mode = "draw"
            if pygame.Rect(340, 10, 80, 40).collidepoint(mx, my):
                mode = "rect"
            if pygame.Rect(430, 10, 80, 40).collidepoint(mx, my):
                mode = "circle"
            if pygame.Rect(520, 10, 80, 40).collidepoint(mx, my):
                mode = "eraser"

            # 3. Қосымша фигураларды таңдау батырмалары
            if pygame.Rect(610, 10, 80, 40).collidepoint(mx, my):
                mode = "square"
            if pygame.Rect(700, 10, 80, 40).collidepoint(mx, my):
                mode = "rtriangle"
            if pygame.Rect(610, 60, 80, 40).collidepoint(mx, my):
                mode = "etriangle"
            if pygame.Rect(700, 60, 80, 40).collidepoint(mx, my):
                mode = "rhombus"

        # Тышқан батырмасын жібергенде (фигураны сызу)
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # Төртбұрыш сызу
            if mode == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(end_pos[0] - start_pos[0])
                h = abs(end_pos[1] - start_pos[1])
                pygame.draw.rect(screen, current_color, (x, y, w, h), 3)

            # Шеңбер сызу (радиусын Пифагор теоремасымен есептеу)
            if mode == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

            # Квадрат сызу (ені мен биіктігі бірдей)
            if mode == "square":
                size = abs(end_pos[0] - start_pos[0])
                pygame.draw.rect(screen, current_color, (*start_pos, size, size), 3)

            # Тік бұрышты үшбұрыш сызу
            if mode == "rtriangle":
                pygame.draw.polygon(screen, current_color, [
                    start_pos,
                    (start_pos[0], end_pos[1]),
                    end_pos
                ], 3)

            # Тең қабырғалы (немесе тең бүйірлі) үшбұрыш сызу
            if mode == "etriangle":
                pygame.draw.polygon(screen, current_color, [
                    (start_pos[0], end_pos[1]),
                    (end_pos[0], end_pos[1]),
                    ((start_pos[0] + end_pos[0]) // 2, start_pos[1])
                ], 3)

            # Ромб сызу
            if mode == "rhombus":
                cx = (start_pos[0] + end_pos[0]) // 2
                cy = (start_pos[1] + end_pos[1]) // 2
                pygame.draw.polygon(screen, current_color, [
                    (cx, start_pos[1]),   # Жоғарғы нүкте
                    (end_pos[0], cy),     # Оң жақ нүкте
                    (cx, end_pos[1]),     # Төменгі нүкте
                    (start_pos[0], cy)    # Сол жақ нүкте
                ], 3)

    # Еркін сызу режимі (тышқан басулы кезінде үздіксіз сызу)
    if drawing and mode == "draw":
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, current_color, last_pos, current_pos, 5)
        last_pos = current_pos

    # Өшіргіш режимі (ақ түсті шеңбермен суретті өшіру)
    if drawing and mode == "eraser":
        pygame.draw.circle(screen, WHITE, pygame.mouse.get_pos(), 15)

    # --- ИНТЕРФЕЙС (Панельдерді салу) ---
    
    # Түс таңдау панелін салу
    for i, c in enumerate(colors):
        pygame.draw.rect(screen, c, (10 + i*50, 10, 40, 40))

    # Ескі режим батырмаларының фоны
    pygame.draw.rect(screen, GRAY, (250, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (340, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (430, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (520, 10, 80, 40))

    # Батырмаларға мәтін жазу
    screen.blit(font.render("Draw", True, BLACK), (265, 20))
    screen.blit(font.render("Rect", True, BLACK), (355, 20))
    screen.blit(font.render("Circle", True, BLACK), (440, 20))
    screen.blit(font.render("Eraser", True, BLACK), (525, 20))

    # Жаңа фигуралар батырмаларының фоны
    pygame.draw.rect(screen, GRAY, (610, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (700, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (610, 60, 80, 40))
    pygame.draw.rect(screen, GRAY, (700, 60, 80, 40))

    # Жаңа фигураларға мәтін жазу
    screen.blit(font.render("Square", True, BLACK), (615, 20))
    screen.blit(font.render("RTri", True, BLACK), (710, 20))
    screen.blit(font.render("ETri", True, BLACK), (615, 70))
    screen.blit(font.render("Rhomb", True, BLACK), (705, 70))

    # Экранды жаңарту
    pygame.display.flip()
    # Кадр жиілігін 60 FPS-ке шектеу
    clock.tick(60)