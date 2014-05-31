
import pygame

import base
import color
import events
import util



class GameView(base.Module):
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
        pass
        if isinstance(event, events.MouseClick):
            pass

        #self.handler.post_event(events.GetUser())

    def update(self):
        pass


class Game(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
