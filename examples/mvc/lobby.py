
import pygame

import base
import events
import util

class Lobby(base.Module):
    GREETING   = "Hello, {}!"
    RETURN_KEY = 13

    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.user = None
        self.hello = util.Label(
            self.background,
            (self.width / 2, 15),
            pygame.font.SysFont("monospace", 14),
            Lobby.GREETING
            )
        label_y = self.height / 10
        self.users_label = util.Label(
            self.background,
            (self.width / 6, label_y),
            self.font,
            "Current users"
            )
        self.users = util.ListBox(
            self.background,
            (150, 300),
            (250, self.height * 3 / 4),
            pygame.font.SysFont("monospace", 18),
            )
        self.games_label = util.Label(
            self.background,
            (self.width * 5 / 8, label_y),
            self.font,
            "Current games"
            )
        self.games = util.ListBox(
            self.background,
            (550, 225),
            (400, self.height / 2),
            pygame.font.SysFont("monospace", 18),
            )
        self.chat_log = util.ListBox(
            self.background,
            (550, 475),
            (400, 140),
            pygame.font.SysFont("monospace", 14),
            )
        self.chat = util.InputBox(
            self.background,
            (550, 570),
            (400, 40),
            self.font,
            30
            )
        self.draw_set.extend([
            self.hello,
            self.users,
            self.games,
            self.users_label,
            self.games_label,
            self.chat_log,
            self.chat
            ])

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            self.chat.try_click(event.pos)
        elif isinstance(event, events.UserUpdate):
            self.user = event.user
            self.reload_users()
        elif isinstance(event, events.KeyPress):
            if event.key == Lobby.RETURN_KEY and self.chat.active and len(self.chat.text) > 0:
                print "saying: {}".format(self.chat.text)
            elif self.chat.active:
                self.chat.input(event.key)


    def reload_users(self):
        print "reloading user"
        self.hello.text = Lobby.GREETING.format(self.user.name)
        self.games.list = self.user.games
        self.users.list = self.user.users


    def update(self):
        if self.user is None:
            self.handler.post_event(events.GetUser())
        self.draw()

