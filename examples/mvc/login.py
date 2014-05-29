
import pygame

import base
import color
import events
import util


class LoginView(base.View):
    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)
        self.errors = ""
        self.error_rect = self.background.get_rect()
        self.error_rect.bottom += 40

        self.name_label = util.Label(
            self.background,
            (400, 160),
            self.font,
            "name"
        )

        self.name_input = util.InputBox(
            self.background,
            (400, 200),
            (400, 40),
            self.font,
            30
        )

        self.server_label = util.Label(
            self.background,
            (400, 260),
            self.font,
            "server"
        )

        self.server_input = util.InputBox(
            self.background,
            (400, 300),
            (400, 40),
            self.font,
            30
        )

        self.login_button = util.Button(
            self.background,
            (400, 400),
            (150, 40),
            color.LightGray,
            self.font,
            "register"
        )

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            if self.name_input.collidepoint(event.pos):
                self.name_input.active = True
            else:
                self.name_input.active = False
            if self.server_input.collidepoint(event.pos):
                self.server_input.active = True
            else:
                self.server_input.active = False
            if self.login_button.collidepoint(event.pos):
                self.send_login_request()
        elif isinstance(event, events.KeyPress):
            if event.key == 13: # enter button
                self.send_login_request()
            elif self.name_input.active:
                self.name_input.input(event.key)
            elif self.server_input.active:
                self.server_input.input(event.key)
        elif isinstance(event, events.LoginError):
            self.errors = event.msg

    def send_login_request(self):
        self.handler.post_event(
            events.TryLogin(
                self.name_input.text,
                self.server_input.text
            )
        )

    def draw(self):
        self.background.fill(color.Gray)

        self.background.blit(
            self.font.render(self.errors, 1, color.Black),
            self.error_rect
        )

        self.name_label.draw()
        self.server_label.draw()

        self.name_input.draw()
        self.server_input.draw()
        self.login_button.draw()
