
import pygame

import base
import color
import events


class LobbyView(base.View):
    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            self.handler.post_event(events.GetUsers())
        elif isinstance(event, events.Users):
            print "Users:\n" + "\n".join(user for user in event.users)

    def draw(self):
        self.background.fill(color.Green)
        self.background.blit(
            self.font.render(str(type(self)), 1, color.Black),
            self.background.get_rect()
        )
