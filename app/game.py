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
# four users limit
# game = name, ids, list of users, limit
class Game(base.Module):
    def __init__(self, handler):
        base.Module.__init__(self, handler)
        self.background_color = color.Blue
        self.font = pygame.font.SysFont("monospace", 15)

        self.game_id = 0     # id of game in the network mgr
        self.user_idx = 0    # position of user in the player_list
        self.won = False
        self.box_list = [None, None, None, None]
        
        self.level_list = [0, 0, 0, 0]
        self.word_list = [
            "cat",
            "dog",
            "rabbit",
            "mouse",
            "bird",
            "horse",
            "cow",
            "chicken",
            "tuna",
            "zebra"]
        
        # text input box for user to type into
        self.word_input = util.InputBox(
            self.background,
            (600, 500),
            (200, 30),
            self.font,
            30
            )
        self.word_input.active = True

        self.cur_word_box = util.TextBox(
            self.background,
            (600, 550),
            (200, 30),
            self.font, 
            self.get_word()
            )

        for i in range(0,4):
            temp_box = util.TextBox(
                self.background,
                ( 60 + i * 110, 500),
                (100, 100),
                self.font,
                "default"
                )
            self.box_list[i] = temp_box

        #self.my_boxes = BoxCollection("bob", self.background, self.font)
    
        #self.handler.post_event(events.GetPlayers())
        #self.handler.post_event(events.GetWords())
        
        self.draw_set.extend(self.box_list)
        self.draw_set.extend([self.word_input, self.cur_word_box])    
            

    # give each box a new height dimension
    def grow_boxes(self):
        for i, box in enumerate(self.box_list):        
            self.box_list[i].top = 450 - (10 * self.level_list[i])

    # get a word for the user to type
    def get_word(self):
        if len(self.word_list) > 0:
            return self.word_list.pop()


    def update(self):
        #if self.won == True:
        #    print "game: posting playerwon"
        #    self.handler.post_event(events.PlayerWon(self.game_id, self.user_idx))
            # display a victory message
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
                    self.handler.post_event(events.GameUpdateOut(
                        self.game_id,
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
            
                elif self.word_input.active:
                    self.word_input.input(event.key)
                    if self.word_input.text == self.cur_word_box.text:
                        self.handler.post_event(events.GameUpdateOut(
                        self.game_id,
                        self.user_idx,
                        self.level_list
                        ))
                        self.word_input.clear()
                        next_word = self.get_word()
                        if next_word != None:
                            self.cur_word_box.text = next_word
                        else:
                            print "ran out of words"

            # send the input box the character that the user typed, display it
            #self.word_input.input(event.key)

            # check to see if the input box text matches the cur_word text
            #if self.word_input.text == self.cur_word_box.text:
                # tell the sever that we moved
            #    self.handler.post_event(events.PlayerSuccess())
            #    # reset the displayed word to be the next word in local word list
            #    self.cur_word_box.text = self.get_word()


