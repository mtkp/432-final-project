
import pygame

import base
import color
import events
import util


class LoginView(base.View):
    RETURN_KEY = 13

    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)

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

        self.error_label = util.Label(
            self.background,
            (400, 500),
            pygame.font.SysFont("monospace", 16),
            "",
            color.Red
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
            if event.key == LoginView.RETURN_KEY:
                self.send_login_request()
            elif self.name_input.active:
                self.name_input.input(event.key)
            elif self.server_input.active:
                self.server_input.input(event.key)
        elif isinstance(event, events.LoginError):
            self.error_label.text = event.msg

    def send_login_request(self):
        self.error_label.text = ""
        self.handler.post_event(
            events.TryLogin(
                self.name_input.text,
                self.server_input.text
            )
        )

    def draw(self):
        self.background.fill(color.Gray)

        self.name_label.draw()
        self.server_label.draw()

        self.name_input.draw()
        self.server_input.draw()
        self.login_button.draw()

        self.error_label.draw()
