# File:         lobby.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse

# Assignment:   Final Project

# Description:

# python modules
import random

# 3rd party modules
import pygame

# our modules
import base
import color
import events
import util


class LobbyGame(object):
    '''Class for representing the game object, which was passed by the
    server, in a way that is useful for the lobby.
    '''
    def __init__(self, game_tuple):
        self.name, self.game_id, self.size, self.limit = game_tuple

    def __str__(self):
        return "'{0.name}' ({0.size}/{0.limit})".format(self)


class Lobby(base.Module):
    GREETING = random.choice([
        "hello, {}!",
        "nihao, {}!",
        "aloha, {}!",
        "hola, {}!",
        "konnichiwa, {}!",
        "guten tag, {}!",
        "bonjour, {}!"
        ])
    RETURN_KEY = 13

    def __init__(self, handler, model):
        base.Module.__init__(self, handler, model)
        self.background_color = color.GameBackground

        # top bar
        self.hello = util.Label(
            self.background,
            (400, 20),
            pygame.font.SysFont("monospace", 15),
            Lobby.GREETING
            )
        self.logout_button = util.Button(
            self.background,
            (730, 20),
            (120, 25),
            color.LightGray,
            pygame.font.SysFont("monospace", 15),
            "unregister"
            )

        # set up left half of screen
        users_label = util.Label(
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
            (340, 32),
            self.font,
            20
            )

        # set up right half of screen
        games_label = util.Label(
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
        create_game_label = util.Label(
            self.background,
            (460, 500),
            pygame.font.SysFont("monospace", 16),
            "game name"
            )
        self.create_game_input = util.InputBox(
            self.background,
            (640, 500),
            (260, 32),
            self.font,
            20
            )
        self.create_game_button = util.Button(
            self.background,
            (650, 550),
            (150, 32),
            color.LightGray,
            self.font,
            "create game"
            )

        self.draw_set.extend([
            self.hello,
            self.logout_button,
            self.users_box,
            self.games_box,
            self.chat_log,
            self.chat_input,
            self.create_game_input,
            self.create_game_button,
            users_label,
            games_label,
            create_game_label
            ])

    def notify(self, event):
        if isinstance(event, events.MouseClick):
            self.chat_input.try_click(event.pos)
            self.create_game_input.try_click(event.pos)
            if self.create_game_button.collidepoint(event.pos):
                self.send_create_game_request()
            elif self.logout_button.collidepoint(event.pos):
                self.handler.post_event(events.Logout())
            elif self.games_box.collidepoint(event.pos):
                game = self.games_box.get_item(event.pos)
                if game:
                    self.handler.post_event(events.TryJoinGame(game.game_id))
        elif isinstance(event, events.ModelUpdated):
            self.reload()
        elif isinstance(event, events.KeyPress):
            if event.key == Lobby.RETURN_KEY \
                and self.chat_input.active \
                    and len(self.chat_input.text) > 0:
                self.handler.post_event(events.TrySendChat(self.chat_input.text))
                self.chat_input.clear()
            elif self.chat_input.active:
                self.chat_input.input(event.key)
            elif self.create_game_input.active:
                self.create_game_input.input(event.key)

    def send_create_game_request(self):
        game_name = self.create_game_input.text
        if len(game_name) > 0:
            self.handler.post_event(events.TryCreateGame(game_name))

    def reload(self):
        self.hello.text     = Lobby.GREETING.format(self.model.username)
        self.games_box.list = [LobbyGame(g) for g in self.model.all_games]
        self.users_box.list = self.model.all_users
        self.chat_log.list  = self.model.chat_log
        self.create_game_input.clear()


