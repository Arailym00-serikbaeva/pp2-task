import pygame
import random
import sys
import os

# Pygame-ді іске қосу
pygame.init()

# Экран өлшемдері мен тақырыбы
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("racer")

# Уақытты (FPS) бақылау үшін таймер
clock = pygame.time.Clock()

# Негізгі түстер
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Көлік суретін жүктеу және өлшемін өзгерту
BASE_DIR = os.path.dirname(__file__)
img_path = os.path.join(BASE_DIR, "car1.png")

base_car = pygame.image.load(img_path).convert_alpha()
base_car = pygame.transform.scale(base_car, (60, 90))

# Көліктің түсін өзгертуге арналған функция (фильтр арқылы)
def tint_image(image, color):
    tinted = image.copy()
    tinted.fill(color, special_flags=pygame.BLEND_RGB_MULT)
    return tinted

# Қарсылас көліктердің мүмкін болатын түстері
colors = [
    (255, 0, 0),
    (0, 200, 0),
    (0, 0, 255),
    (255, 0, 255),
    (255, 255, 255)
]

# Ойыншының көлігін баптау
player_img = tint_image(base_car, (0, 150, 255))
player = player_img.get_rect(center=(250, 600))

# Жолдағы 3 жолақтың орталық координаталары
lanes = [170, 250, 330]

# Қарсыластар тізімі және олардың бастапқы жылдамдығы
enemies = []
enemy_speed = 3

# Жаңа қарсылас көлікті кездейсоқ жерден шығару функциясы
def spawn_enemy():
    lane = random.choice(lanes)
    color = random.choice(colors)
    img = tint_image(base_car, color)
    rect = img.get_rect(center=(lane, -100))
    enemies.append({"img": img, "rect": rect})

# Тиындардың түрлері (түсі мен құндылығы)
coin_types = [
    {"color": (255, 215, 0), "value": 1},   # Әдеттегі (алтын)
    {"color": (0, 255, 255), "value": 2},   # Сирек (көгілдір)
    {"color": (255, 0, 255), "value": 3}    # Супер (күлгін)
]

coins = []
score = 0
font = pygame.font.SysFont(None, 40)

# Тиындарды кездейсоқ жолақтарда шығару функциясы
def spawn_coin():
    lane = random.choice(lanes)
    coin_type = random.choice(coin_types)
    coin = {
        "rect": pygame.Rect(lane, -30, 30, 30),
        "color": coin_type["color"],
        "value": coin_type["value"]
    }
    coins.append(coin)

# Жолдың қозғалысын имитациялауға арналған айнымалы
road_offset = 0

# Жолды салу функциясы
def draw_road():
    global road_offset
    screen.fill((200, 200, 200)) # Шөптің түсі
    pygame.draw.rect(screen, GRAY, (100, 0, 300, HEIGHT)) # Асфальт

    # Ақ үзік сызықтардың қозғалысы
    road_offset += 5
    if road_offset >= 40:
        road_offset = 0

    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (200, y + road_offset, 10, 25))
        pygame.draw.rect(screen, WHITE, (290, y + road_offset, 10, 25))

# Ойын деңгейін (жылдамдықты) бақылау
last_level = 0
frame = 0
running = True

# --- НЕГІЗГІ ОЙЫН ЦИКЛІ ---
while running:
    clock.tick(60) # 60 FPS
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Басқару: Солға және оңға көрсеткіштері
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 7
    if keys[pygame.K_RIGHT]:
        player.x += 7

    # Көліктің жол жиегінен шығып кетпеуін қадағалау
    if player.left < 100:
        player.left = 100
    if player.right > 400:
        player.right = 400

    # Белгілі бір уақыт аралығында жаңа нысандарды шығару
    if frame % 80 == 0:
        spawn_enemy()
    if frame % 140 == 0:
        spawn_coin()

    # Қарсыластар қозғалысы мен соқтығысуды тексеру
    for enemy in enemies[:]:
        enemy["rect"].y += enemy_speed
        if enemy["rect"].y > HEIGHT:
            enemies.remove(enemy)

        # Апат болған жағдайда ойынды тоқтату
        if player.colliderect(enemy["rect"]):
            pygame.quit()
            sys.exit()

    # Тиындар қозғалысы мен жинауды тексеру
    for coin in coins[:]:
        coin["rect"].y += enemy_speed
        if coin["rect"].y > HEIGHT:
            coins.remove(coin)

        # Ойыншы тиынды алса, ұпай қосылады
        if player.colliderect(coin["rect"]):
            score += coin["value"]
            coins.remove(coin)

    # Әрбір 5 ұпай сайын жылдамдықты арттыру (қиындату)
    if score // 5 > last_level:
        enemy_speed += 0.5
        last_level += 1

    # Экранды суреттеу
    draw_road()
    screen.blit(player_img, player) # Ойыншы

    for enemy in enemies:
        screen.blit(enemy["img"], enemy["rect"]) # Қарсыластар

    for coin in coins:
        pygame.draw.circle(screen, coin["color"], coin["rect"].center, 12) # Тиындар

    # Ұпайды экранға шығару
    text = font.render(f"Coins: {score}", True, BLACK)
    screen.blit(text, (WIDTH - 180, 15))

    pygame.display.flip()

# Ойыннан шығу
pygame.quit()
sys.exit()