#!/usr/bin/python2.7

import pygame
import os

import base
import color
import events
import util

# player represents by the stack of words that he/she has completed so far
# 
class Player(object):
    def __init__(self, username):
        # words is a list of label objects
        self.words = []
        self.username = username
        

    # add a wor
    def add_word(self, word):
        # make a new label object
        label = util.TextBox(
            self.background,
            # width, height)
        self.words.append(label)
    
    
    def draw():
        
        

# Ideas for the view:
#   * highlight letters as correct
#   * automatically move on to next word once the correct characters are typed
#   * show words on side of screen that users are getting right or wrong
class Game(base.Module):
    def __init__(self, handler, window):
        base.Module.__init__(self, handler, window)
        self.background_color = color.Blue

        # hashmap of usernames to listboxes for opponents
        self.player_list = []
        self.word_list = []
        self.should_move = False
        self.won = False

        self.handler.post_event(events.GetPlayers())
        self.handler.post_event(events.GetWords())

        self.label = util.Label(
            self.background,
            (400, 300),
            self.font,
            str(type(self))
            )

        # input box for player to type word into
        input_box_height = self.height / 15
        self.word_input = util.InputBox(
            self.background,
            (self.width / 2, self.height / 2),
            (self.width / 2, input_box_height),
            self.font,
            30
            )
        self.word_input.active == true

        # 
        self.cur_word_box = util.TextBox(
            self.background,
            (self.width / 2, 260),
            self.font,
            self.get_word()         # get the first word from the list
            #get next word
            )
        self.draw_set.extend([
            self.word_input,
            self.cur_word_box,
            
            })
            # player list
            

    # get a word for the user to type
    def get_word(self):
        if len(self.wordlist) > 0:
            return self.wordlist.pop
        else:
            # if no more words, player one
            self.handler.post_event(events.PlayerWon())
         

    def update(self):
        if self.should_move == True:
            self.handler.post_event(events.PlayerMoved())
            self.cur_word_box.text = self.get_word()
            self.should_move = False
        elif self.won == True:
            self.handler.post_event(events.PlayerWon())
            # display a victory message
        self.draw()
        

    def notify(self, event):
        if isinstance(event, events.StartGame()):
            # set the games player list to be the list of names from server
            
        elif isinstance(event, events.OpponentSuccess()):
            # find opponent in local collection of opponents
            # with that player, call addword method
            pass
        elif isinstance(event, events.OpponentWon()):
            # maybe print which opponent won text and return to lobby
            self.handler.post_event(events.EndGame())
            pass
        elif isinstance(event, events.OpponentGone()):
            # remove locally
            #
            pass
        elif isinstance(event, events.KeyPress):
            # send the input box the character that the user typed, display it
            self.word_input.input(event.key)    
            # check to see if the input box text matches the cur_word text
            if self.word_input.text == self.cur_word_box.text:
                # tell the sever that we moved
                self.handler.post_event(events.PlayerMoved())
                # reset the displayed word to be the next word in local word list
                self.cur_word_box.text = self.get_word()



