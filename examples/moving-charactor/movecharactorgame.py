#!/usr/bin/python2.7

# code taken from:
# https://bitbucket.org/r1chardj0n3s/pygame-tutorial/src

import pygame

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('player.png')
        self.original = pygame.image.load('player.png')
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
            self._spin()
        elif key[pygame.K_d]:
            self._spin()
            
    def _spin(self):
        "spin the player image"
        center = self.rect.center
        self.angle = self.angle + 12
        if self.angle >= 360:
            self.angle = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=center)
            

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

