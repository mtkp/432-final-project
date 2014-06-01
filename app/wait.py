
import pygame

import base
import color
import events
import util


class Wait(base.Module):
    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.font = pygame.font.SysFont("monospace", 40)
        self.background_color = color.Green
        # set up left half of screen
        self.label = util.Label(
            self.background,
            (400, 300),
            self.font,
            "1 / 4"
            )

        self.draw_set.extend([
            self.label
            ])

    def notify(self, event):
        pass

    def update(self):
        self.draw()

