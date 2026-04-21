import pygame

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Paint")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

color = BLACK


screen.fill(WHITE)

drawing = False
start_pos = (0, 0)

tool = "brush"  

clock = pygame.time.Clock()
running = True


while running:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

       
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        
        if event.type == pygame.KEYDOWN:

           
            if event.key == pygame.K_b:
                tool = "brush"

            elif event.key == pygame.K_r:
                tool = "rectangle"

            elif event.key == pygame.K_c:
                tool = "circle"

            elif event.key == pygame.K_e:
                tool = "eraser"

            
            elif event.key == pygame.K_1:
                color = (255, 0, 0)   

            elif event.key == pygame.K_2:
                color = (0, 255, 0)   

            elif event.key == pygame.K_3:
                color = (0, 0, 255)   

            elif event.key == pygame.K_4:
                color = (0, 0, 0)     

    
    if drawing:

        
        if tool == "brush":
            pygame.draw.circle(screen, color, (mx, my), 5)

        
        elif tool == "eraser":
            pygame.draw.circle(screen, WHITE, (mx, my), 10)

        
        elif tool == "rectangle":
            width = mx - start_pos[0]
            height = my - start_pos[1]
            pygame.draw.rect(screen, color,
                             (start_pos[0], start_pos[1], width, height), 2)

        
        elif tool == "circle":
            radius = int(((mx - start_pos[0]) ** 2 +
                          (my - start_pos[1]) ** 2) ** 0.5)
            pygame.draw.circle(screen, color, start_pos, radius, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()