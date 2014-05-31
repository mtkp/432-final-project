

import pygame
import os

import base
import color
import events
import util

img_folder = "images"
success_increment

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        
        # access image in subfolder, os-independant        
        img_name = ".png"
        try:
            self.image = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
            self.imageMaster = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
        except:
            raise UserWarning, "Unable to find the images in the folder" + \
                                img_folder

        
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())

        
    # should update the vertical postion of the player by a set increment
    # if the word was spelled correctly
    def update(self):
        if isinstance(event, events.WordSuccess):
            # notify the serevr by posting event to 
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
        if isinstance(event, events.WordSuccess):
            self.handler.post_event(events.PlayerMoved())
        if isinstance(event, events.OpponentMoved())
        pass
        


class Game(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)


