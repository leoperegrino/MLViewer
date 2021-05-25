#!/bin/python
# vim: foldnestmax=2 foldlevel=1
import Models
import pygame
import sys
from pygame.surfarray import pixels2d
from pygame.locals import *
from pygame.colordict import THECOLORS as COLOR

class Game:
    """
    """
    def __init__(self, RES_X=600, RES_Y=600):
        """
        """
        pygame.init()
        pygame.mouse.set_visible(False)

        self.RES = { 'X': RES_X, 'Y': RES_Y }
        self.DISPLAY = pygame.display.set_mode((RES_X, RES_Y))
        self.PLOT = pygame.Surface((RES_X, RES_Y))
        self.CLOCK = pygame.time.Clock()
        self.FONT_SIZE = 26
        self.FONT = pygame.font.SysFont(None, self.FONT_SIZE)


    def mouse_track(self, y, color=COLOR['red']):
        """
        uses array of pixels of the plot surface to paint current height position.
        updates the array by shifting first half pixels to 1 pixel before.

        px(t, x-1) := px(t-1, x)

        ++---        -++--
        ++---   :=   -++--
        ++---        -++--

        """
        # reference plot surface pixels. locks the surface
        pixels = pixels2d(self.PLOT)

        # use mouse height to paint a pixel at middle
        pixels[self.RES['X'] // 2, y] = self.PLOT.map_rgb(color)

        # set pixels equals to next one, provides time feeling
        pixels[:self.RES['X'] // 2, :] = pixels[1:self.RES['X'] // 2 + 1, :]

        # unlocks surface
        del pixels

        # blit the surface onto display
        self.DISPLAY.blit(self.PLOT, (0,0))


    def print_stats(self, stats, position):
        """
        stats: model stats
        position: top left corner of stats
        """
        for key, val in stats.items():
            stat_str = f'{key} = {str(val)[:6]}'
            stat_text = self.FONT.render(stat_str, True, COLOR['green'])
            self.DISPLAY.blit(stat_text, position)
            position[1] += self.FONT_SIZE

    def _check_events(self):
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
                    self.RUNNING = False if self.RUNNING else True


    def run(self, model):
        """
        """
        self.model = model(self.PLOT)
        self.RUNNING = True
        while True:
            if self.RUNNING:
                self.iterate()
                self._check_events()
                # redraw screen
                pygame.display.update()
                # loop at `tick` fps
                self.CLOCK.tick(60)


    def iterate(self):
        """
        """
        x, y = pygame.mouse.get_pos()

        self.model.append(y)
        self.model.show()

        stats = self.model.stats()
        stats['x'] = x
        stats['y'] = y

        self.mouse_track(y)
        self.print_stats(stats, [50,50])

        pygame.draw.circle(self.DISPLAY, COLOR['green'], (x,y), radius=10)


def main():
    game=Game()
    game.run(Models.Linear)

if __name__ == "__main__":
    main()
