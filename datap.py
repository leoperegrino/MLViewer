#!/bin/python
import pygame
from pygame.locals import *
import sys

RES = (600, 600)
BLACK = pygame.Color(0,0,0)
GREEN = pygame.Color(0,255,0)

pygame.init()
clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode(RES)

text = pygame.font.SysFont(None, 32)

while True: # main game loop

    DISPLAYSURF.fill(BLACK)

    # mouse position tuple unpacking
    x, y = pygame.mouse.get_pos()
    x_str = f'w = {str(x)}'
    y_str = f'h = {str(y)}'
    xSurfText = text.render(x_str, True, GREEN)
    ySurfText = text.render(y_str, True, GREEN)
    DISPLAYSURF.blit(xSurfText, (100,100))
    DISPLAYSURF.blit(ySurfText, (100,150))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # leave with escape
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
    pygame.display.update()
    clock.tick(60)
