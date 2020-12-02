import pygame
from pygame.locals import QUIT
import sys

RES = (600, 600)
BG = pygame.Color(0,0,0)
GREEN = pygame.Color(0,255,0)

pygame.init()

DISPLAYSURF = pygame.display.set_mode(RES)

text = pygame.font.Font(pygame.font.get_default_font(), 32)

while True: # main game loop

    DISPLAYSURF.fill(BG)
    mouse = pygame.mouse.get_pos()
    pos = f'w = {str(mouse[0])} - h = {str(mouse[1])}'

    textSurfaceObj = text.render(pos, True, GREEN)

    DISPLAYSURF.blit(textSurfaceObj, (100,100))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

