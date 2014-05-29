
import pygame

import base
import color
import events


class GameView(base.View):
    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)

    def notify(self, event):
        pass

    def draw(self):
        self.background.fill(color.Blue)
        self.background.blit(
            self.font.render(str(type(self)), 1, color.Black),
            self.background.get_rect()
        )


class Game(base.Model):
    def __init__(self, handler):
        base.Model.__init__(self, handler)
