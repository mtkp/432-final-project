
import pygame

import base
import color
import events
import util


class GameWait(base.Module):
    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.font = pygame.font.SysFont("monospace", 60)
        self.background_color = color.GameBackground
        # set up left half of screen

        self.label = util.Label(
            self.background,
            (400, 300),
            self.font,
            "1 / 4" # stub this out for now... eventually will need to put real count here
            )

        self.exit_button = util.Button(
            self.background,
            (400, 550),
            (120, 25),
            color.LightGray,
            pygame.font.SysFont("monospace", 15),
            "leave game"
            )

        self.draw_set.extend([
            self.label,
            self.exit_button
            ])

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            if self.exit_button.collidepoint(event.pos):
                self.handler.post_event(events.LeaveGame())

    def update(self):
        self.draw()

