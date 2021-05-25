#!/bin/python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from pygame.surfarray import pixels2d
from pygame.colordict import THECOLORS as COLOR

class Data():
    """
    Base class for managing data
    """
    def __init__(self, size):
       self.size = size
       self.X = np.arange(size).reshape(-1, 1)
       self.Y = np.full(size, size).reshape(-1, 1)

    def append(self, value):
        self.Y[:self.size - 1, 0] = self.Y[1:self.size + 1, 0]
        self.Y[self.size - 1, 0] = value


class Model(Data):
    """
    Base class for models
    """
    def __init__(self, bg, model):
       super().__init__(bg.get_height()//2)
       self.bg = bg
       self.model = model

    def calculate(self):
        self.model.fit(self.X, self.Y)
        self.data = self.model.predict(self.X + self.size)

    def show(self):
        self.calculate()

        pixels = pixels2d(self.bg)
        pixels[self.size:, :] = self.bg.map_rgb(COLOR['black'])

        for i, px in enumerate(self.data):
            if px >= self.size*2: px = self.size*2 - 1
            if px <= 0: px = 0
            pixels[i + self.size, int(px)] = self.bg.map_rgb(COLOR['yellow'])

        del pixels


class Linear(Model):
    """
    Linear Regression model
    """
    def __init__(self, bg):
       super().__init__(bg, LinearRegression())

    def stats(self):
        self.stats_ = {}
        self.stats_['Coefficient'] = float(self.model.coef_)
        self.stats_['Intercept'] = float(self.model.intercept_)
        self.stats_['Score'] = float(self.model.score(self.X, self.Y))
        return self.stats_


class Logistic(Model):
    """
    Logistic Regression model
    """
    def __init__(self, bg):
       super().__init__(bg, LogisticRegression())
