import pygame
import random
import sys
import os

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)

BASE_DIR = os.path.dirname(__file__)
img_path = os.path.join(BASE_DIR, "car.png")

base_car = pygame.image.load(img_path).convert_alpha()
base_car = pygame.transform.scale(base_car, (60, 90))

def tint_image(image, color):
    tinted = image.copy()
    tinted.fill(color, special_flags=pygame.BLEND_RGB_MULT)
    return tinted

colors = [
    (255, 0, 0),
    (0, 200, 0),
    (0, 0, 255),
    (255, 0, 255),
    (255, 255, 255)
]

player_img = tint_image(base_car, (0, 150, 255))
player = player_img.get_rect(center=(250, 600))

lanes = [170, 250, 330]

enemies = []
enemy_speed = 3

def spawn_enemy():
    lane = random.choice(lanes)
    color = random.choice(colors)
    img = tint_image(base_car, color)
    rect = img.get_rect(center=(lane, -100))
    enemies.append({"img": img, "rect": rect})

coins = []
score = 0
font = pygame.font.SysFont(None, 40)

def spawn_coin():
    x = random.choice(lanes)
    coins.append(pygame.Rect(x, -30, 30, 30))

road_offset = 0

def draw_road():
    global road_offset

    screen.fill((200, 200, 200))
    pygame.draw.rect(screen, GRAY, (100, 0, 300, HEIGHT))

    road_offset += 5
    if road_offset >= 40:
        road_offset = 0

    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (200, y + road_offset, 10, 25))
        pygame.draw.rect(screen, WHITE, (290, y + road_offset, 10, 25))

frame = 0
running = True

while running:
    clock.tick(60)
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 7
    if keys[pygame.K_RIGHT]:
        player.x += 7

    if player.left < 100:
        player.left = 100
    if player.right > 400:
        player.right = 400

    if frame % 80 == 0:
        spawn_enemy()

    if frame % 140 == 0:
        spawn_coin()

    for enemy in enemies[:]:
        enemy["rect"].y += enemy_speed

        if enemy["rect"].y > HEIGHT:
            enemies.remove(enemy)

        if player.colliderect(enemy["rect"]):
            pygame.quit()
            sys.exit()

    for coin in coins[:]:
        coin.y += enemy_speed

        if coin.y > HEIGHT:
            coins.remove(coin)

        if player.colliderect(coin):
            coins.remove(coin)
            score += 1

    if frame % 400 == 0:
        enemy_speed += 0.5

    draw_road()

    screen.blit(player_img, player)

    for enemy in enemies:
        screen.blit(enemy["img"], enemy["rect"])

    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin.center, 12)

    text = font.render(f"Coins: {score}", True, BLACK)
    screen.blit(text, (WIDTH - 180, 15))

    pygame.display.flip()

pygame.quit()
sys.exit()