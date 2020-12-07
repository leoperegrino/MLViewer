#!/bin/python
import pygame
from pygame.surfarray import pixels2d
from pygame.locals import *
import sys

# constants
RES = (600, 600)
BLACK = pygame.Color(0,0,0)
GREEN = pygame.Color(0,255,0)
RED = pygame.Color(255,0,0)

pygame.init()

DISPLAY = pygame.display.set_mode(RES)
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 32)

pygame.mouse.set_visible(False)

PLOT = pygame.Surface(RES)

# main game loop
while True:
    DISPLAY.fill(BLACK)

    # mouse position tracking
    # tuple unpacking:
    x, y = pygame.mouse.get_pos()
    # use mouse height to paint a pixel at middle
    pixels2d(PLOT)[RES[0]//2, y] = 0xFF0000
#     pixels2d(PLOT)[RES[0]//2, y] = PLOT.map_rgb(RED)
    # set pixels equals to next one, provides time feeling
    pixels2d(PLOT)[:RES[0]//2,:] = pixels2d(PLOT)[1:RES[0]//2 + 1,:]
    # reset the mid ones so they don't keep appearing
    pixels2d(PLOT)[RES[0]//2 ,:] = 0
    # blit the surface
    DISPLAY.blit(PLOT, (0,0))

    # use circle as mouse
    pygame.draw.circle(DISPLAY, (0,255,0,100), (x, y), 15)

    # string to be displyed:
    x_str = 'w = ' + str(x)
    y_str = 'h = ' + str(y)
    # render the string with font obj:
    xText = FONT.render(x_str, True, GREEN)
    yText = FONT.render(y_str, True, GREEN)
    # display text onto bg:
    DISPLAY.blit(xText, (100,100))
    DISPLAY.blit(yText, (100,150))

    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # leave with escape
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    # redraw screen
    pygame.display.update()
    # loop at 60fps
    CLOCK.tick(60)
