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

            for i, c in enumerate(colors):
                if pygame.Rect(10 + i*50, 10, 40, 40).collidepoint(mx, my):
                    current_color = c

            if pygame.Rect(250, 10, 80, 40).collidepoint(mx, my):
                mode = "draw"
            if pygame.Rect(340, 10, 80, 40).collidepoint(mx, my):
                mode = "rect"
            if pygame.Rect(430, 10, 80, 40).collidepoint(mx, my):
                mode = "circle"
            if pygame.Rect(520, 10, 80, 40).collidepoint(mx, my):
                mode = "eraser"

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if mode == "rect":
                end_pos = event.pos
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(end_pos[0] - start_pos[0])
                h = abs(end_pos[1] - start_pos[1])
                pygame.draw.rect(screen, current_color, (x, y, w, h), 3)

            if mode == "circle":
                end_pos = event.pos
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

   
    if drawing and mode == "draw":
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, current_color, last_pos, current_pos, 5)
        last_pos = current_pos

    if drawing and mode == "eraser":
        pygame.draw.circle(screen, WHITE, pygame.mouse.get_pos(), 15)


    for i, c in enumerate(colors):
        pygame.draw.rect(screen, c, (10 + i*50, 10, 40, 40))

  
    pygame.draw.rect(screen, GRAY, (250, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (340, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (430, 10, 80, 40))
    pygame.draw.rect(screen, GRAY, (520, 10, 80, 40))

    screen.blit(font.render("Draw", True, BLACK), (265, 20))
    screen.blit(font.render("Rect", True, BLACK), (355, 20))
    screen.blit(font.render("Circle", True, BLACK), (440, 20))
    screen.blit(font.render("Eraser", True, BLACK), (525, 20))

    pygame.display.flip()
    clock.tick(60)