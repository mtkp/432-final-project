
import pygame

import base
import color
import events
import util

class GameView(base.View):
    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)
        self.background_color = color.Blue
        self.label = util.Label(
            self.background,
            (400, 300),
            self.font,
            str(type(self))
            )

    def notify(self, event):
        pass


class Game(base.Model):
    def __init__(self, handler):
        base.Model.__init__(self, handler)
