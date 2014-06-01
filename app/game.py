
import pygame

import base
import color
import events
import util


class Game(base.Module):
    def __init__(self, handler, window):
        base.Module.__init__(self, handler, window)
        self.background_color = color.Blue
        self.label = util.Label(
            self.background,
            (400, 300),
            self.font,
            str(type(self))
            )

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            pass

        #self.handler.post_event(events.GetUser())

    def update(self):
        pass
