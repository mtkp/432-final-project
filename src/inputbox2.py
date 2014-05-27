#!/usr/bin/python2.7

import pygame, string
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GRAY  = (195, 195, 195)

class InputBox2(object):
    "a text input box for getting user input"
    def __init__(self, screenObj, colortup, width, height, left, top, message, 
                 sequenceNum):
        self.message = message
        self.background = screenObj
        self.LEFT_EDGE = self.background.get_rect().left
        self.TOP_EDGE = self.background.get_rect().top
        self.MARGIN = 5

        self.width = width
        self.height = height
        self.left = left
        self.top = top + (sequenceNum * (height + self.MARGIN))

        self.box_surface = pygame.Surface((width, height))
        self.box_surface.fill(colortup)
        self.box_surface_pos = self.box_surface.get_rect()
        self.box_surface_pos.left = left
        self.box_surface_pos.top = top
        self.background.blit(self.box_surface, self.box_surface_pos)


    # if the given box has focus, get the input for it
    def get_input_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                return event.key
            else:
                pass

    def display_box(self, message):
        fontobject = pygame.font.Font(None,18)

        pygame.draw.rect(self.background, WHITE,
                         (self.left, self.top, self.width, self.height), 0)

        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, BLACK),
                        self.LEFT_EDGE + self.MARGIN, 
                        self.TOP_EDGE + 50)
                        #+ self.sequenceNum

        pygame.display.flip()

    def ask(self, screen):
        "ask(screen, question) -> answer"
        pygame.font.init()
        current_string = []
        display_box(self.background, self.message + ": " + 
            string.join(current_string,""))

        while 1:
            inkey = get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == K_RETURN:
                break
            elif inkey <= 127:
                current_string.append(chr(inkey))
                display_box(screen, self.message + ": " + 
                    string.join(current_string,""))

        return string.join(current_string,"")



