import pygame
import random

pygame.init()


WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


snake_pos = [100, 100]
snake_body = [[100, 100], [90, 100], [80, 100]]

direction = "RIGHT"
change_to = direction


def generate_food():
    """Food snake үстіне түспейтіндей генерацияланады"""
    while True:
        food = [random.randrange(0, WIDTH, 10),
                random.randrange(0, HEIGHT, 10)]
        if food not in snake_body:
            return food

food_pos = generate_food()


score = 0
level = 1
speed = 10

font = pygame.font.SysFont("Arial", 20)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = "UP"
            elif event.key == pygame.K_DOWN:
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT:
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT:
                change_to = "RIGHT"

    direction = change_to


    if direction == "UP":
        snake_pos[1] -= 10
    if direction == "DOWN":
        snake_pos[1] += 10
    if direction == "LEFT":
        snake_pos[0] -= 10
    if direction == "RIGHT":
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))

    
    if snake_pos == food_pos:
        score += 1
        food_pos = generate_food()
    else:
        snake_body.pop()

    
    if score % 4 == 0 and score != 0:
        level = score // 4 + 1
        speed = 10 + level * 2

    if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
        running = False


    for block in snake_body[1:]:
        if snake_pos == block:
            running = False


    for block in snake_body:
        pygame.draw.rect(screen, GREEN, (*block, 10, 10))

    pygame.draw.rect(screen, RED, (*food_pos, 10, 10))


    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()