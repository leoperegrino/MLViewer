#!/bin/python
import Models
import pygame
import numpy as np
import sys
from pygame.surfarray import pixels2d
from pygame.locals import *
from pygame.colordict import THECOLORS as COLOR
from sklearn.linear_model import LinearRegression

def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    # constants
    RES_X = 600
    RES_Y = 600
    RES = (RES_X, RES_Y)
    DISPLAY = pygame.display.set_mode(RES)
    PLOT = pygame.Surface(RES)
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont(None, 32)


    def mouse_track(y, color=COLOR['red']):
        """
        uses array of pixels of the plot surface to paint current height position.
        updates the array by shifting first half pixels to 1 pixel before.
        px(t, x-1) := px(t-1, x), as shown below:

        ++---        -++--
        ++---   :=   -++--
        ++---        -++--

        """
        # reference plot surface pixels. locks the surface
        pixels = pixels2d(PLOT)

        # use mouse height to paint a pixel at middle
        pixels[RES_X // 2, y] = PLOT.map_rgb(color)

        # set pixels equals to next one, provides time feeling
        pixels[:RES_X // 2, :] = pixels[1:RES_X // 2 + 1, :]

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
        xText = FONT.render(x_str, True, COLOR['green'])
        yText = FONT.render(y_str, True, COLOR['green'])

        # display text onto bg:
        DISPLAY.blit(xText, x_loc)
        DISPLAY.blit(yText, y_loc)


    linear = Models.Linear(PLOT)
    RUNNING = True

    # main game loop
    while True:
        if RUNNING:
            DISPLAY.fill(COLOR['black'])

            x, y = pygame.mouse.get_pos()

            mouse_track(y)
            print_coord(x, y)

            linear.append(y)
            linear.show()

            pygame.draw.circle(DISPLAY, COLOR['green'], (x,y), radius=10)

        # events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # leave with escape
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                # (un)pause with space
                if event.key == K_SPACE:
                    if RUNNING:
                        RUNNING = False
                    else:
                        RUNNING = True
        # redraw screen
        pygame.display.update()
        # loop at 60fps
        CLOCK.tick(60)

if __name__ == "__main__":
    main()
