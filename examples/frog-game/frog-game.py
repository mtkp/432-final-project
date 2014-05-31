

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
        # notify the server by posting event to event handler
        # increment the user's player postion by set increment
            

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
        

    def notify(self, event):
        # if the user gets a word right, send event to the server
        if isinstance(event, events.WordSuccess()):
            self.handler.post_event(events.PlayerMoved())
            
        if isinstance(event, events.OpponentMoved())
            # how do we move those opponent sprites individually?
            # find opponent in model's local collection of opponents
            # that opponent's update function should move him 
            pass
        


class Game(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
            

