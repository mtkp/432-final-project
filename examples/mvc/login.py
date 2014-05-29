
import pygame

import base
import color
import events


class LoginView(base.View):
    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)
        self.errors = ""
        self.error_rect = self.background.get_rect()
        self.error_rect.bottom += 40

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            self.handler.post_event(events.TryLogin("matt", "localhost"))
        elif isinstance(event, events.LoginError):
            self.errors = event.msg

    def draw(self):
        self.background.fill(color.Red)
        self.background.blit(
            self.font.render(str(type(self)), 1, color.Black),
            self.background.get_rect()
        )

        self.background.blit(
            self.font.render(self.errors, 1, color.Black),
            self.error_rect
        )

        self.window.blit(self.background, self.background.get_rect())