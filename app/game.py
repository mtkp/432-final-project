# File:         game.py

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

GAME_WORD_COUNT = 15

class State:
    PLAYING  = 0
    GAMEOVER = 1

class Game(base.Module):
    def __init__(self, handler, model):
        base.Module.__init__(self, handler, model)
        self.background_color = color.Blue
        self.font = pygame.font.SysFont("monospace", 20)
        self.reload()

    # listen for update event
    def notify(self, event):
        if self.state == State.GAMEOVER:
            if isinstance(event, events.MouseClick):
                self.handler.post_event(events.EndGame())
        else:
            if isinstance(event, events.GameInitialize):
                self.users = event.user_names
                self.words = event.words
                self.refresh_user_names()
                self.refresh_game_input()
            elif isinstance(event, events.PlayerWon):
                self.state = State.GAMEOVER
                self.make_ending(event.msg)
            elif isinstance(event, events.GameUpdateIn):
                self.level_list = event.level_list
                self.move_user_boxes()
            elif isinstance(event, events.KeyPress):
                self.word_input.input(event.key)
                if self.word_input.text == self.cur_word_box.text:
                    self.handler.post_event(events.GameUpdateOut(
                        self.model.username
                        ))
                    self.refresh_game_input()

    # only display boxes for users in the current game (maybe someone left)
    def make_user_boxes(self):
        for i in xrange(4):
            temp_box = util.TextBox(
                self.background,
                (100 + i * 200, 400),
                (175, 50),
                pygame.font.SysFont("monospace", 16),
                ""
                )
            temp_box.set_text_color(color.White)
            temp_box.set_box_color(color.DarkRed)
            self.box_list[i] = temp_box

        self.draw_set.extend(self.box_list)

    def refresh_user_names(self):
        for box, username in zip(self.box_list, self.users):
            box.text = username[:16]
            if username == self.model.username:
                box.set_box_color(color.Green)

    def refresh_game_input(self):
        self.word_input.clear()
        try:
            self.cur_word_box.text = self.words.pop()
        except IndexError:
            pass

    # give each box a new height dimension
    def move_user_boxes(self):
        incr = 300 / GAME_WORD_COUNT
        for box, level in zip(self.box_list, self.level_list):
            box.top = 75 + (incr * (GAME_WORD_COUNT - level))

    def make_ending(self, msg):
        self.draw_set.append(
            util.TextBox(
                self.background,
                (400, 300),
                (600, 200),
                pygame.font.SysFont("monospace", 24),
                msg
                )
            )
        self.draw_set.append(
            util.TextBox(
                self.background,
                (400, 500),
                (350, 200),
                pygame.font.SysFont("monospace", 18),
                "click anywhere to continue..."
                )
            )

    def reload(self):
        self.draw_set = []
        self.state = State.PLAYING

        self.box_list = [None, None, None, None]
        self.level_list = [0, 0, 0, 0]
        self.words = []
        self.users = []
        for i in range(self.model.current_game[3]):
            self.users.append("")

        # text input box for user to type into
        self.word_input = util.InputBox(
            self.background,
            (400, 560),
            (320, 45),
            self.font,
            25
            )
        self.word_input.active = True

        # box to display the current word user should type
        self.cur_word_box = util.TextBox(
            self.background,
            (400, 500),
            (320, 45),
            self.font
            )
        self.cur_word_box.set_box_color(color.Gray)
        self.cur_word_box.set_box_color(color.LightGray)

        # represent the target to the user
        finish_line = util.Box(
            self.background,
            (400, 75),
            (775, 8),
            color.Green
            )

        self.draw_set.extend([
            finish_line,
            self.word_input,
            self.cur_word_box
            ])
        self.make_user_boxes()



