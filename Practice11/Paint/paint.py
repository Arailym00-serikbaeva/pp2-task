import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

colors = [BLACK, RED, GREEN, BLUE]
current_color = BLACK

mode = "draw"

drawing = False
start_pos = None
last_pos = None

font = pygame.font.SysFont(None, 24)

screen.fill(WHITE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            mx, my = event.pos

            # 🎨 выбор цвета
            for i, c in enumerate(colors):
                if pygame.Rect(10 + i*50, 10, 40, 40).collidepoint(mx, my):
                    current_color = c

            # 🧰 кнопки режимов
            if pygame.Rect(250, 10, 80, 40).collidepoint(mx, my):
                mode = "draw"
            if pygame.Rect(340, 10, 80, 40).collidepoint(mx, my):
                mode = "rect"
            if pygame.Rect(430, 10, 80, 40).collidepoint(mx, my):
                mode = "circle"
            if pygame.Rect(520, 10, 80, 40).collidepoint(mx, my):
                mode = "eraser"

            # 🆕 новые фигуры
            if pygame.Rect(610, 10, 80, 40).collidepoint(mx, my):
                mode = "square"
            if pygame.Rect(700, 10, 80, 40).collidepoint(mx, my):
                mode = "rtriangle"
            if pygame.Rect(610, 60, 80, 40).collidepoint(mx, my):
                mode = "etriangle"
            if pygame.Rect(700, 60, 80, 40).collidepoint(mx, my):
                mode = "rhombus"

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            end_pos = event.pos

            # прямоугольник
            if mode == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(end_pos[0] - start_pos[0])
                h = abs(end_pos[1] - start_pos[1])
                pygame.draw.rect(screen, current_color, (x, y, w, h), 3)

            # круг
            if mode == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

            # 🟩 квадрат
            if mode == "square":
                size = abs(end_pos[0] - start_pos[0])
                pygame.draw.rect(screen, current_color, (*start_pos, size, size), 3)

            # 🔺 прямоугольный треугольник
            if mode == "rtriangle":
                pygame.draw.polygon(screen, current_color, [
                    start_pos,
                    (start_pos[0], end_pos[1]),
                    end_pos
                ], 3)

            # 🔺 равносторонний треугольник
            if mode == "etriangle":
                pygame.draw.polygon(screen, current_color, [
                    (start_pos[0], end_pos[1]),
                    (end_pos[0], end_pos[1]),
                    ((start_pos[0] + end_pos[0]) // 2, start_pos[1])
                ], 3)

            # 💎 ромб
            if mode == "rhombus":
                cx = (start_pos[0] + end_pos[0]) // 2
                cy = (start_pos[1] + end_pos[1]) // 2

                pygame.draw.polygon(screen, current_color, [
                    (cx, start_pos[1]),
                    (end_pos[0], cy),
                    (cx, end_pos[1]),
                    (start_pos[0], cy)
                ], 3)

    # ✏️ рисование
    if drawing and mode == "draw":
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, current_color, last_pos, current_pos, 5)
        last_pos = current_pos

    # 🧽 ластик
    if drawing and mode == "eraser":
        pygame.draw.circle(screen, WHITE, pygame.mouse.get_pos(), 15)

    # 🎨 панель цветов
    for i, c in enumerate(colors):
        pygame.draw.rect(screen, c, (10 + i*50, 10, 40, 40))

    # 🧰 кнопки режимов (старые)
    pygame.draw.rect(screen, GRAY, (250, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (340, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (430, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (520, 10, 80, 40))

    screen.blit(font.render("Draw", True, BLACK), (265, 20))
    screen.blit(font.render("Rect", True, BLACK), (355, 20))
    screen.blit(font.render("Circle", True, BLACK), (440, 20))
    screen.blit(font.render("Eraser", True, BLACK), (525, 20))

    # 🆕 новые кнопки
    pygame.draw.rect(screen, GRAY, (610, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (700, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (610, 60, 80, 40))
    pygame.draw.rect(screen, GRAY, (700, 60, 80, 40))

    screen.blit(font.render("Square", True, BLACK), (615, 20))
    screen.blit(font.render("RTri", True, BLACK), (710, 20))
    screen.blit(font.render("ETri", True, BLACK), (615, 70))
    screen.blit(font.render("Rhomb", True, BLACK), (705, 70))

    pygame.display.flip()
    clock.tick(60)