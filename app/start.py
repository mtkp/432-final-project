
import pygame

import base
import color
import util


class Start(base.Module):
    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.background_color = color.GameBackground
        self.font = pygame.font.SysFont("monospace", 50)

        label = util.Label(
            self.background,
            (self.width / 2, 200),
            self.font,
            "type it"
            )
        help_label = util.Label(
            self.background,
            (self.width / 2, 400),
            pygame.font.SysFont("monospace", 30),
            "click anywhere to begin"
            )
        self.draw_set.extend([
            label,
            help_label
            ])

    def update(self):
        self.draw()

