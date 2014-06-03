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


class Login(base.Module):
    TAB_KEY = 9
    RETURN_KEY = 13

    def __init__(self, handler, model):
        base.Module.__init__(self, handler, model)
        self.background_color = color.GameBackground

        input_box_height = self.height / 15
        name_label = util.Label(
            self.background,
            (self.width / 2, 160),
            self.font,
            "name"
            )
        self.name_input = util.InputBox(
            self.background,
            (self.width / 2, self.height / 3),
            (self.width / 2, input_box_height),
            self.font,
            30
            )
        server_label = util.Label(
            self.background,
            (self.width / 2, 260),
            self.font,
            "server"
            )
        self.server_input = util.InputBox(
            self.background,
            (self.width / 2, self.height / 2),
            (self.width / 2, input_box_height),
            self.font,
            30
            )
        self.login_button = util.Button(
            self.background,
            (self.width / 2, self.height * 4 / 6),
            (self.width / 7, input_box_height),
            color.LightGray,
            self.font,
            "register"
            )
        self.error_label = util.Label(
            self.background,
            (self.width / 2, self.height * 5 / 6),
            pygame.font.SysFont("monospace", 16),
            "",
            color.Red
            )
        self.draw_set.extend([
            self.error_label,
            self.login_button,
            self.server_input,
            self.name_input,
            server_label,
            name_label
            ])

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            self.name_input.try_click(event.pos)
            self.server_input.try_click(event.pos)
            if self.login_button.collidepoint(event.pos):
                self.send_login_request()
        elif isinstance(event, events.KeyPress):
            if event.key == Login.TAB_KEY:
                self.name_input.active, self.server_input.active = \
                    self.server_input.active, self.name_input.active
            if event.key == Login.RETURN_KEY:
                self.send_login_request()
            elif self.name_input.active:
                self.name_input.input(event.key)
            elif self.server_input.active:
                self.server_input.input(event.key)
        elif isinstance(event, events.LoginError):
            self.error_label.text = event.msg

    def send_login_request(self):
        self.error_label.text    = ""
        self.name_input.active   = False
        self.server_input.active = False
        self.handler.post_event(
            events.TryLogin(
                self.name_input.text,
                self.server_input.text
                )
            )

    def reload(self):
        self.name_input.active = True

