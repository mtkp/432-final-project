#!/usr/bin/python2.7

import pygame
import os
import copy

import base
import color
import events
import util

RETURN_KEY = 13
TAB_KEY = 9

# 800 x 600 width x height

# player represents by the stack of words that he/she has completed so far
class BoxCollection(object):
    def __init__(self, username, background, font):

        self.box_list = []          # list of the TextBox objects to dislay
        self.username = username
        self.background = background
        self.index = 0
    
        for i in range(4):
            temp_box = util.TextBox(
                background,
                ( 60 + i * 110, 500),
                (100, 100),
                font,
                username
                )
            self.box_list.append(temp_box)


    def grow_boxes(self, level_list):
        for i, box in enumerate(self.box_list):        
            box.height = 100 + (10 * level_list[i])
            #box.centery = 550 - (10 * level_list[i])
            

    def draw(self):
        for box in self.box_list:
            box.draw()        

# four users limit
# game = name, ids, list of users, limit
class Game(base.Module):
    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.background_color = color.Blue


        self.game_id = 0     # id of game in the network mgr
        self.user_idx = 0    # position of user in the player_list

        self.box_list = [None, None, None, None]
        for i in range(0,4):
            temp_box = util.TextBox(
                self.background,
                ( 60 + i * 110, 500),
                (100, 100),
                pygame.font.SysFont("monospace", 15),
                "default"
                )
            self.box_list[i] = temp_box


        self.level_list = [0, 0, 0, 0]
        self.word_list = []
        self.should_move = False
        self.won = False
        #self.my_boxes = BoxCollection("bob", self.background, self.font)
    
        #self.handler.post_event(events.GetPlayers())
        #self.handler.post_event(events.GetWords())
        
        self.draw_set.extend(self.box_list)
            
            #self.level_list
            #self.word_input
            

    # give each box a new height dimension
    def grow_boxes(self):
        for i, box in enumerate(self.box_list):        
            box.height = 100 + (10 * self.level_list[i])
            #box.centery = 550 - (10 * level_list[i])

    # get a word for the user to type
    def get_word(self):
        if len(self.word_list) > 0:
            return self.wordlist.pop
        else:
            # if no more words, player won
            self.handler.post_event(events.PlayerWon())


    def update(self):
        #if self.won == True:
        #    print "game: posting playerwon"
        #    self.handler.post_event(events.PlayerWon(self.game_id, self.user_idx))
            # display a victory message
        self.grow_boxes()
        self.draw()


    # listen for update event and take list of ints from it.
    # another success, user listens for this and sends to server
    def notify(self, event):
        if isinstance(event, events.StartGame):
            self.user_list = event.level_list
        elif isinstance(event, events.GameUpdateIn):
            if event.game_id == self.game_id:
                print "game: got gameupdatein"
                self.level_list = event.level_list
                self.grow_boxes()            
        elif isinstance(event, events.OpponentWon):
            # maybe print which opponent won text and return to lobby
            self.handler.post_event(events.EndGame)
        elif isinstance(event, events.KeyPress):
            if isinstance(event, events.KeyPress):
                if event.key == RETURN_KEY:
                    print "game: pressed enter"
                    self.handler.post_event(events.GameUpdateOut(self.game_id,
                                                                 self.user_idx,
                                                                 self.level_list))
                if event.key == TAB_KEY:
                    print "game: pressed tab"
                    #new_levels = copy.deepcopy(self.level_list)
                    #new_levels[self.user_idx] += 1
                    self.level_list[0] += 1    
                    self.grow_boxes()
                    #self.handler.post_event(events.GameUpdateIn(self.game_id,
                    #                                           new_levels))



            ## send the input box the character that the user typed, display it
            #self.word_input.input(event.key)

            ## check to see if the input box text matches the cur_word text
            #if self.word_input.text == self.cur_word_box.text:
            #    # tell the sever that we moved
            #    self.handler.post_event(events.PlayerSuccess())
            #    # reset the displayed word to be the next word in local word list
            #    self.cur_word_box.text = self.get_word()


