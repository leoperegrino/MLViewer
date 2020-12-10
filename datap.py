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
PLOT = pygame.Surface(RES)

pygame.mouse.set_visible(False)

def mouse_track(y, color=RED):
    """
    uses array of pixels of the plot surface to paint current position.
    updates the array by shifting first half pixels to 1 pixel before.
    as shown below:

    -++--        ++---
    -++--   :=   ++---
    -++--        ++---

    """
    X = RES[0]

    # reference plot surface pixels. locks the surface
    pixels = pixels2d(PLOT)

    # use mouse height to paint a pixel at middle
    pixels[X // 2, y] = PLOT.map_rgb(color)

    # set pixels equals to next one, provides time feeling
    pixels[:X // 2, :] = pixels[1:X // 2 + 1, :]

    # reset the mid ones so they don't keep appearing
    pixels[X //2 ,:] = 0

    # unlocks surface
    del pixels

    # blit the surface onto display
    DISPLAY.blit(PLOT, (0,0))

def print_coord(x, y, x_loc=(100,100), y_loc=(100,150)):
    """
    x, y: coordinates to render over display
    x_loc, y_loc: where to render the text over the display
    """
    # string to be displyed:
    x_str = 'w = ' + str(x)
    y_str = 'h = ' + str(y)

    # render the string with font obj:
    xText = FONT.render(x_str, True, GREEN)
    yText = FONT.render(y_str, True, GREEN)

    # display text onto bg:
    DISPLAY.blit(xText, x_loc)
    DISPLAY.blit(yText, y_loc)

# main game loop
while True:
    DISPLAY.fill(BLACK)

    x, y = pygame.mouse.get_pos()

    mouse_track(y)
    print_coord(x, y)

    pygame.draw.circle(DISPLAY, GREEN, (x,y), 10)

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
