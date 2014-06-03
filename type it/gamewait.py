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
import events
import util


class GameWait(base.Module):
    def __init__(self, handler, model):
        base.Module.__init__(self, handler, model)
        self.font = pygame.font.SysFont("monospace", 72)
        self.background_color = color.GameBackground

        self.label = util.Label(
            self.background,
            (400, 300),
            self.font,
            str(self.model.current_game[2]) + " / 4"
            )

        self.exit_button = util.Button(
            self.background,
            (400, 550),
            (120, 25),
            color.LightGray,
            pygame.font.SysFont("monospace", 15),
            "leave game"
            )

        self.pending_dot = util.Box(
            self.background,
            (350, 450),
            (20, 20),
            color.Blue
            )
        self.dot_ticks = 0

        self.draw_set.extend([
            self.label,
            self.exit_button,
            self.pending_dot
            ])

    def draw(self):
        self.dot_ticks += 1
        if self.dot_ticks == 15:
            self.dot_ticks = 0
            self.pending_dot.centerx += 25
            if self.pending_dot.centerx == 475:
                self.pending_dot.centerx = 350
        base.Module.draw(self)

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            if self.exit_button.collidepoint(event.pos):
                self.handler.post_event(events.LeaveGame())
        elif isinstance(event, events.ModelUpdated):
            self.label.text = str(self.model.current_game[2]) + " / 4"
