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
    FONT = pygame.font.SysFont(None, 26)


    def mouse_track(y, color=COLOR['red']):
        """
        uses array of pixels of the plot surface to paint current height position.
        updates the array by shifting first half pixels to 1 pixel before.

        px(t, x-1) := px(t-1, x)

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


    def print_stats(stats, position):
        """
        stats: model stats
        position: top left corner of stats
        """
        for key, val in stats.items():
            stat_str = f'{key} = {str(val)[:6]}'
            stat_text = FONT.render(stat_str, True, COLOR['green'])
            DISPLAY.blit(stat_text, position)
            position[1] += 20


    linear = Models.Linear(PLOT)
    RUNNING = True

    # main game loop
    while True:
        if RUNNING:

            x, y = pygame.mouse.get_pos()

            linear.append(y)
            linear.show()

            stats = linear.stats()
            stats['x'] = x
            stats['y'] = y

            mouse_track(y)
            print_stats(stats, [50,50])

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
        # loop at tick fps
        CLOCK.tick(60)

if __name__ == "__main__":
    main()
