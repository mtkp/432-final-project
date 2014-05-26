#! /usr/bin/python2.7

import pygame

class ListBox():
    # screenObj - which surface to draw onto
    # colortup  - color to fill box. ex: (255,255,255)
    # x & y     - coordinates to draw the box at
    # height & width - dimensions of the rect
    def __init__(self, screenObj, colortup, width, height, x, y, left, top):
        # make a box to display text items in
        self.name = name
        self.user_box = pygame.Surface((250, 400))
        self.user_box.fill(colortup)
        self.user_box_pos = user_box.get_rect()
        self.user_box_pos.left = left
        self.user_box_pos.top = top
        screenObj.blit(self.user_box, self.user_box_pos)
        return (self.user_box, self.user_box_pos)

    # render the list of users in the users box
    def display_items(self, items):
        # for each item in list
        for item in items:
            #make a line of text to display
            #get the rect for it
            #position the rect in the list
            #display the rect 

