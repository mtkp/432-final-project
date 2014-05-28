#!/usr/bin/python2.7

import color
import rect

class Game(object):
    def __init__(self, background, user):
        self.background = rect.Rectangle(
            background,
            (400, 300),
            (800, 600),
            color.Green
        )

    def update(self):
        pass

    def draw(self):
        self.background.draw()
