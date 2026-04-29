import pygame
import random
import sys

pygame.init()

# размеры окна
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# размер блока
BLOCK = 20

# начальная змейка
snake = [[300, 300], [280, 300], [260, 300]]
direction = "RIGHT"

# 🍎 разные типы еды (цвет + очки)
food_types = [
    {"color": (255, 0, 0), "value": 1},
    {"color": (0, 255, 0), "value": 2},
    {"color": (0, 0, 255), "value": 3}
]

# генерация еды
def spawn_food():
    while True:
        x = random.randrange(0, WIDTH, BLOCK)
        y = random.randrange(0, HEIGHT, BLOCK)

        if [x, y] not in snake:
            f = random.choice(food_types)

            return {
                "pos": [x, y],
                "color": f["color"],
                "value": f["value"],
                "timer": 200  # ⏳ время жизни еды
            }

food = spawn_food()

# счёт и уровень
score = 0
level = 1
speed = 10

font = pygame.font.SysFont(None, 36)

# главный цикл
running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # движение головы
    head = snake[0].copy()

    if direction == "UP":
        head[1] -= BLOCK
    elif direction == "DOWN":
        head[1] += BLOCK
    elif direction == "LEFT":
        head[0] -= BLOCK
    elif direction == "RIGHT":
        head[0] += BLOCK

    # ❗ столкновение со стеной
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # ❗ столкновение с собой
    if head in snake:
        pygame.quit()
        sys.exit()

    snake.insert(0, head)

    # 🍽️ проверка еды
    if head == food["pos"]:
        score += food["value"]  # учитываем вес еды
        food = spawn_food()
    else:
        snake.pop()

    # ⏳ таймер еды (исчезает)
    food["timer"] -= 1
    if food["timer"] <= 0:
        food = spawn_food()

    # 📈 уровень каждые 4 очка
    if score // 4 + 1 > level:
        level += 1
        speed += 2

    # рисуем
    screen.fill(BLACK)

    # змейка
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, BLOCK, BLOCK))

    # 🍎 еда с цветом
    pygame.draw.rect(screen, food["color"], (*food["pos"], BLOCK, BLOCK))

    # текст
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()