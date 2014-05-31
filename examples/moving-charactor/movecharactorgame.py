#!/usr/bin/python2.7

# code taken from:
# https://bitbucket.org/r1chardj0n3s/pygame-tutorial/src

import pygame
import os

img_folder = "images"

class Weapon():
    def __init__(self, *groups):
        super(Weapon, self).__init__(*groups)
        
        # # access image in subfolder, os-independant
        img_name = "player.png"
        try:
            self.image = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
            self.imageMaster = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
        except:
            raise UserWarning, "Unable to find the images in the folder" + \
                                img_folder

    def update(self):
        pass
        


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        
        # access image in subfolder, os-independant        
        img_name = "player.png"
        try:
            self.image = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
            self.imageMaster = pygame.image.load(os.path.join(img_folder,
                                                                 img_name))
        except:
            raise UserWarning, "Unable to find the images in the folder" + \
                                img_folder

        
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())
        self.angle = 0
        

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 10
        if key[pygame.K_RIGHT]:
            self.rect.x += 10
        if key[pygame.K_UP]:
            self.rect.y -= 10
        if key[pygame.K_DOWN]:
            self.rect.y += 10
        
        if key[pygame.K_a]:
            self._turn_left()
            self._update_rotation()
        elif key[pygame.K_d]:
            self._turn_right()
            self._update_rotation()
    
    def _update_rotation(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter    

    def _turn_left(self):
        self.angle += 12
        if self.angle > 360:
            self.angle = 0
    
    def _turn_right(self):
        self.angle -= 12
        if self.angle < 0:
            self.angle = 360
            
    def _spin(self, direction):
        "spin the player image"
        center = self.rect.center
        
            

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        sprites = pygame.sprite.Group()
        self.player = Player(sprites)
        
        # list of opponents

        while 1:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            sprites.update()
            screen.fill((200, 200, 200))
            sprites.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)

