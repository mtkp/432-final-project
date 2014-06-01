
import pygame

import base
import color
import util


class Start(base.Module):
    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.background_color = color.DarkGreen
        self.font = pygame.font.SysFont("monospace", 40)

        label = util.Label(
            self.background,
            (self.width / 2, 200),
            self.font,
            "type it",
            color.White
            )
        help_label = util.Label(
            self.background,
            (self.width / 2, 400),
            pygame.font.SysFont("monospace", 20),
            "click anywhere to begin",
            color.White
            )
        self.draw_set.extend([
            label,
            help_label
            ])

    def update(self):
        self.draw()

