
#

# File:         .py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:


import pygame

import base
import color
import util


class Start(base.Module):
    def __init__(self, handler, model):
        base.Module.__init__(self, handler, model)
        self.background_color = color.GameBackground
        self.font = pygame.font.SysFont("monospace", 60)

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