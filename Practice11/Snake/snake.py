import pygame
import random
import sys

# Pygame-ді іске қосу
pygame.init()

# Терезе өлшемдері
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Жылан ойыны")

# Кадр жиілігін (жылдамдықты) бақылау
clock = pygame.time.Clock()

# Түстер
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Жыланның әр блогының өлшемі
BLOCK = 20

# Жыланның бастапқы денесі (үш блок) және қозғалыс бағыты
snake = [[300, 300], [280, 300], [260, 300]]
direction = "RIGHT"

# Тамақтың түрлері: түсі мен беретін ұпайы
food_types = [
    {"color": (255, 0, 0), "value": 1},   # Қызыл - 1 ұпай
    {"color": (0, 255, 0), "value": 2},   # Жасыл - 2 ұпай
    {"color": (0, 0, 255), "value": 3}    # Көк - 3 ұпай
]

# Тамақты кездейсоқ жерден шығару функциясы
def spawn_food():
    while True:
        x = random.randrange(0, WIDTH, BLOCK)
        y = random.randrange(0, HEIGHT, BLOCK)

        # Тамақ жыланның денесінде пайда болмауы керек
        if [x, y] not in snake:
            f = random.choice(food_types)

            return {
                "pos": [x, y],
                "color": f["color"],
                "value": f["value"],
                "timer": 200  # Тамақтың өмір сүру уақыты (цикл саны)
            }

# Бірінші тамақты шығару
food = spawn_food()

# Ұпай, деңгей және жылдамдық
score = 0
level = 1
speed = 10

font = pygame.font.SysFont(None, 36)

# --- НЕГІЗГІ ОЙЫН ЦИКЛІ ---
running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Басқару: бағытты өзгерту (кері бұрылуға болмайды)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Жылан басының жаңа орнын есептеу
    head = snake[0].copy()

    if direction == "UP":
        head[1] -= BLOCK
    elif direction == "DOWN":
        head[1] += BLOCK
    elif direction == "LEFT":
        head[0] -= BLOCK
    elif direction == "RIGHT":
        head[0] += BLOCK

    # Қабырғаға соғылуды тексеру
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # Өз денесіне соғылуды тексеру
    if head in snake:
        pygame.quit()
        sys.exit()

    # Жаңа басты тізімнің алдына қосу
    snake.insert(0, head)

    # Тамақты жегенін тексеру
    if head == food["pos"]:
        score += food["value"]  # Тамақтың түріне қарай ұпай қосу
        food = spawn_food()     # Жаңа тамақ шығару
    else:
        # Егер тамақ желінбесе, құйрығын алып тастау (қозғалыс эффектісі)
        snake.pop()

    # Тамақтың таймерін азайту (уақыты бітсе, тамақ жоғалып, басқа жерден шығады)
    food["timer"] -= 1
    if food["timer"] <= 0:
        food = spawn_food()

    # Әрбір 4 ұпай сайын деңгей мен жылдамдықты арттыру
    if score // 4 + 1 > level:
        level += 1
        speed += 2

    # --- ЭКРАНДЫ СУРЕТТЕУ ---
    screen.fill(BLACK)

    # Жыланды салу
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, BLOCK, BLOCK))

    # Тамақты салу
    pygame.draw.rect(screen, food["color"], (*food["pos"], BLOCK, BLOCK))

    # Ұпай мен деңгейді көрсету
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    # Өзгерістерді экранға шығару
    pygame.display.flip()

pygame.quit()
sys.exit()