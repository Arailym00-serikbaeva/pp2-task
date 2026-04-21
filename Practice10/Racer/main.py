import pygame
import random

#INIT 
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

clock = pygame.time.Clock()

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#LOAD IMAGES
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (60, 60))

coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (30, 30))

#PLAYER
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 80))
player_speed = 6

#COINS
coins = []
coin_count = 0

def spawn_coin():
    """Жоғарыдан кездейсоқ coin шығару"""
    x = random.randint(20, WIDTH - 20)
    coin_rect = coin_img.get_rect(center=(x, -20))
    coins.append(coin_rect)

#FONT
font = pygame.font.SysFont("Arial", 20)

#GAME LOOP
running = True
while running:
    screen.fill(BLACK)

    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #CONTROLS
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed

    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    #COIN LOGIC
    if random.randint(1, 40) == 1:
        spawn_coin()

    for coin in coins[:]:
        coin.y += 5  


        if coin.colliderect(player_rect):
            coins.remove(coin)
            coin_count += 1

        elif coin.top > HEIGHT:
            coins.remove(coin)

    #DRAW
    screen.blit(player_img, player_rect)

    for coin in coins:
        screen.blit(coin_img, coin)

    #COUNTER
    text = font.render(f"Coins: {coin_count}", True, WHITE)
    screen.blit(text, (WIDTH - 130, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()