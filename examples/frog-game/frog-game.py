#!/usr/bin/python2.7

import pygame
import os

import base
import color
import events
import util

img_folder = "images"
increment = 3
start_x = 320
start_y = 240

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)

        self.should_move = False
        img_folder = "images"
        img_name = "frog.png"
        # access image in subfolder, os-independant
        try:
            self.image = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
            self.imageMaster = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
        except:
            raise UserWarning, "Unable to find the images in the folder" + \
                                img_folder
        self.rect = pygame.rect.Rect((start_x, start_y), self.image.get_size())


    # update y coord of player if the word was spelled correctly
    def update(self):
        if self.should_move == True:
            # how do we notify the server?
            self.handler.post_event(events.PlayerMoved())
            self.rect.y -= increment
            should_move = False

# Ideas for the view:
#   * highlight letters as correct
#   * automatically move on to next word once the correct characters are typed
#   * show words on side of screen that users are getting right or wrong
class GameView(base.Module):
    def __init__(self, handler, window):
        base.Module.__init__(self, handler, window)
        self.background_color = color.Blue
        self.label = util.Label(
            self.background,
            (400, 300),
            self.font,
            str(type(self))
            )

        # i think the view should own the sprite group to be updated?
        self.sprites = pygame.sprite.Group()
        self.player = Player(sprites)
        # put in input box
        # put in text that displays word user should type
        # draw vertical lines for lanes for each frog


    def notify(self, event):
        if isinstance(event, events.OpponentMoved()):
            # how do we move those opponent sprites individually?
            # find opponent in model's local collection of opponents
            # that opponent's update function should move him
            pass
        elif isinstance(event, events.OpponentWon()):
            # maybe print which opponent won text and return to lobby
            self.handler.post_event(events.EndGame())
            pass
        elif isinstance(event, events.OpponentGone()):
            # server knows opponent gone, so just remove locally
            # self.sprites.remove()
            pass




class Game(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.wordlist = util.get_words()

    # get a word for the user to type
    def get_word(self):
        if len(self.wordlist) > 0:
            return self.wordlist.pop
        else:
            # if no more words, player one
            self.handler.post_event(events.PlayerWon())




