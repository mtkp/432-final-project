#!/usr/bin/python2.7

import pygame
import os

import base
import color
import events
import util

RETURN_KEY = 13

# 800 x 600 width x height

# player represents by the stack of words that he/she has completed so far
class Player(object):
    def __init__(self, username, background, font):

        self.box_list = []
        self.username = username
        self.background = background
        self.index = 0
<<<<<<< HEAD

=======

>>>>>>> 7e7eacc1b37d9b82d7e2434b1c43941c6f38352b
    # add the next word after current index

        self.box = util.TextBox(
            background,
            (100, 100),
            (100, 100),
            font,
            username
            )
<<<<<<< HEAD

=======

>>>>>>> 7e7eacc1b37d9b82d7e2434b1c43941c6f38352b
    #def add_word(self, word):
    #    box = util.TextBox(
    ##        self.background,
    #        (),
    #        (),
    #        self.font,
    #        word
    #        )
    #    self.box_list.append(box)
    def grow_box(self, index, level):
        self.box.height = level
<<<<<<< HEAD

    # draw each text box in the list
=======

    # draw each text box in the list
>>>>>>> 7e7eacc1b37d9b82d7e2434b1c43941c6f38352b
    def draw(self):
        self.box.draw()
        #for word in
        #for box in self.box_list:
        #    self.box.draw()

# four users limit
# game = name, ids, list of users, limit
class Game(base.Module):
    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.background_color = color.Blue

        self.game_id = 0      # id of game in the network mgr
        #self.user_idx = user_idx    # position of user in the player_list

        self.player_list = []
        self.word_list = []
        self.should_move = False
        self.won = False

        self.handler.post_event(events.GetPlayers())
        self.handler.post_event(events.GetWords())

        self.player1 = Player("bob", self.background, self.font, ) # colmn num

        self.draw_set.extend([
            #self.player_list
            #self.word_input
            self.player1
            ])


    # get a word for the user to type
    def get_word(self):
        if len(self.word_list) > 0:
            return self.wordlist.pop
        else:
            # if no more words, player won
            self.handler.post_event(events.PlayerWon())


    def update(self):
        #if self.should_move == True:
            #
        #elif self.should_move = True
        #    self.handler.post_event(events.PlayerSuccess())
        #    self.handler.post_event(events.PlayerSuccess())
        #    self.cur_word_box.text = self.get_word()
        #    self.should_move = False
        #elif self.won == True:
        #    self.handler.post_event(events.PlayerWon())
        #    self.won = False
        #    # display a victory message
        self.draw()


    # listen for update event and take list of ints from it.
    # another success, user listens for this and sends to server
    def notify(self, event):
        if isinstance(event, events.StartGame):
            self.players_list = event.players_list# set the games player list to be the list of names from server
            pass
        elif isinstance(event, events.GameUpdate):
            self.player_list = event.level_list
            self.should_move = True
        elif isinstance(event, events.OpponentSuccess):
            self.player_list = event.player_list
            # find opponent in local collection of opponents
            # with that player, call addword method
            pass
        elif isinstance(event, events.OpponentWon):
            # maybe print which opponent won text and return to lobby
            self.handler.post_event(events.EndGame)
            pass
        elif isinstance(event, events.OpponentGone):
            # remove locally
            pass
        elif isinstance(event, events.KeyPress):
            if isinstance(event, events.KeyPress):
                if event.key == RETURN_KEY:
                    print "game: pressed enter"
                    self.handler.post_event(events.GameUpdateOut(self.player_list, self.game_id))
            ## send the input box the character that the user typed, display it
<<<<<<< HEAD
            #self.word_input.input(event.key)
=======
            #self.word_input.input(event.key)
>>>>>>> 7e7eacc1b37d9b82d7e2434b1c43941c6f38352b
            ## check to see if the input box text matches the cur_word text
            #if self.word_input.text == self.cur_word_box.text:
            #    # tell the sever that we moved
            #    self.handler.post_event(events.PlayerSuccess())
            #    # reset the displayed word to be the next word in local word list
            #    self.cur_word_box.text = self.get_word()
<<<<<<< HEAD
=======

>>>>>>> 7e7eacc1b37d9b82d7e2434b1c43941c6f38352b


