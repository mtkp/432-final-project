
import pygame

import base
import color
import events


class LobbyView(base.View):
    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)
        self.name = None

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            self.handler.post_event(events.GetUsers())
        elif isinstance(event, events.KeyPress):
            if chr(event.key) == 'q':
                self.handler.post_event(events.Logout())

    def draw(self):
        if self.name is None:
            self.handler.notify
        self.background.fill(color.Green)
        self.background.blit(
            self.font.render(str(type(self)) + " press q to log out", 1, color.Black),
            self.background.get_rect()
        )


class Lobby(base.Model):
    def __init__(self, handler):
        base.Model.__init__(self, handler)

    def notify(self, event):
        if isinstance(event, events.Users):
            print "Users:\n" + "\n".join(user for user in event.users)

