
import random

import pygame

import base
import color
import events
import util


# used for representing the game tuple in the lobby
# this class is NOT actually the game
class LobbyGame(object):
    def __init__(self, game_tuple):
        self.name, self._id, self.size, self.limit = game_tuple[0]

    def __str__(self):
        return "{0.name} ({0.size}/{0.limit})".format(self, self.users)


class Lobby(base.Module):
    GREETING   = random.choice([
        "hello, {}!",
        "nihao, {}!",
        "aloha, {}!",
        "hola, {}!",
        "konnichiwa, {}!",
        "guten tag, {}!",
        "bonjour, {}!"
        ])
    RETURN_KEY = 13

    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.user = None
        self.hello = util.Label(
            self.background,
            (self.width / 2, 15),
            pygame.font.SysFont("monospace", 15),
            Lobby.GREETING
            )

        # set up left half of screen
        self.users_label = util.Label(
            self.background,
            (self.width * 1 / 4, 50),
            self.font,
            "current users"
            )
        self.users_box = util.ListBox(
            self.background,
            (200, 225),
            (340, 325),
            pygame.font.SysFont("monospace", 18),
            )
        self.chat_log = util.ListBox(
            self.background,
            (200, 475),
            (340, 150),
            pygame.font.SysFont("monospace", 14),
            )
        self.chat_input = util.InputBox(
            self.background,
            (200, 575),
            (340, 40),
            self.font,
            30
            )

        # set up right half of screen
        self.games_label = util.Label(
            self.background,
            (self.width * 3 / 4, 50),
            self.font,
            "current games"
            )
        self.games_box = util.ListBox(
            self.background,
            (600, 250),
            (340, 375),
            pygame.font.SysFont("monospace", 18),
            )
        self.create_game_input = util.InputBox(
            self.background,
            (600, 500),
            (260, 40),
            self.font,
            20
            )
        self.create_game_button = util.Button(
            self.background,
            (600, 550),
            (260, 40),
            color.LightGray,
            self.font,
            "create game"
            )

        self.draw_set.extend([
            self.hello,
            self.users_box,
            self.games_box,
            self.users_label,
            self.games_label,
            self.chat_log,
            self.chat_input,
            self.create_game_input,
            self.create_game_button
            ])

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            self.chat_input.try_click(event.pos)
            self.create_game_input.try_click(event.pos)
            if self.create_game_button.collidepoint(event.pos):
                self.send_create_game_request()
        elif isinstance(event, events.UserUpdate):
            self.user = event.user
            self.reload_users()
        elif isinstance(event, events.KeyPress):
            if event.key == Lobby.RETURN_KEY \
                and self.chat_input.active \
                    and len(self.chat_input.text) > 0:
                print "saying: {} (not yet, really)".format(self.chat_input.text)
                self.chat_input.clear()
            elif self.chat_input.active:
                self.chat_input.input(event.key)
            elif self.create_game_input.active:
                self.create_game_input.input(event.key)

    def send_create_game_request(self):
        game_name = self.create_game_input.text
        if len(game_name) > 0:
            "posting create game"
            self.handler.post_event(events.TryCreateGame(game_name))

    def reload_users(self):
        print "reloading user"
        self.hello.text = Lobby.GREETING.format(self.user.name)
        self.games_box.list = self.user.games
        self.users_box.list = self.user.users

    def update(self):
        if self.user is None:
            self.handler.post_event(events.GetUser())
        self.draw()

