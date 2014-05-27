#!/usr/bin/python2.7

import pygame, pygame.draw
from pygame.locals import *

import game2


class InputBox2(object):
    "a text input box for getting user input"
    def __init__(self, screen, colortup, width, height, left, bottom, message,
                 sequence_num):
        self.message = message
        self.background = screen
        self.LEFT_EDGE = self.background.get_rect().left
        self.BOTTOM_EDGE = self.background.get_rect().bottom
        self.MARGIN = 5

        self.width = width
        self.height = height
        self.left = left
        self.bottom = self.BOTTOM_EDGE - (sequence_num * (height + self.MARGIN))

        self.box_surface = pygame.Surface((width, height))
        self.box_surface.fill(colortup)
        self.box_surface_pos = self.box_surface.get_rect()
        self.box_surface_pos.left = left
        self.box_surface_pos.bottom = self.bottom
        self.background.blit(self.box_surface, self.box_surface_pos)

        self.font = pygame.font.Font(None, 20)
        self.display_box(self.message + ": ")


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

    # called each character key is pressed during ask()
    def display_box(self, message):
        print "<message = {}>".format(message)

        pygame.draw.rect(
            self.background,
            game2.WHITE,
            (self.left, self.bottom - self.height, self.width, self.height),
            0
        )

        self.background.blit(
            self.font.render(message, 1, game2.BLACK),
            (self.left, self.bottom - self.height)
        )
        pygame.display.get_surface().blit(self.background, (0,0))
        pygame.display.flip()


    # called when input box gets focus
    def ask(self):
        pygame.font.init()
        current_string = []
        self.display_box(self.message + ": " + "".join(current_string))

        while 1:
            inkey = self.get_input_key()
            if inkey == K_RETURN:
                break
            elif inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
                self.display_box(
                    self.message + ": " + "".join(current_string)
                )
            elif inkey <= 127:
                current_string.append(chr(inkey))
                self.display_box(
                    self.message + ": " + "".join(current_string)
                )

        return "".join(current_string)



