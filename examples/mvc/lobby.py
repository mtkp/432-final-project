
import pygame

import base
import color
import events


class LobbyView(base.View):
    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)

    def notify(self, event):
        pass

    def draw(self):
        self.background.fill(color.Green)
        self.background.blit(
            self.font.render(str(type(self)), 1, color.Black),
            self.background.get_rect()
        )
        self.window.blit(self.background, self.background.get_rect())
