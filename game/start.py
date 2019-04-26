import pygame
from player import *
from obstacle import *

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 30)

player = Player(100, 450, 50, 50)
ob = Obstacle(800, 460, 40, 40)

crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    

    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 800, 600))
    pygame.draw.rect(screen, (0, 0, 0), (0, 502, 800, 200))

    score = myfont.render(str("{:.2f}".format(player.score)), False, (0, 0, 0))
    screen.blit(score ,(50, 50))

    player.render(screen)
    ob.render(screen)

    ob.tick()
    player.tick(ob)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
