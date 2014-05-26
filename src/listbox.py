#!/usr/bin/python2.7

import pygame

class ListBox():
    # screenObj - which surface to draw onto
    # colortup  - color to fill box. ex: (255,255,255)
    # x & y     - coordinates to draw the box at
    # height & width - dimensions of the rect
    def __init__(self, screenObj, colortup, width, height, left, top):
        # make a box to display text items in
        self.user_box = pygame.Surface((250, 400))
        self.user_box.fill(colortup)
        self.user_box_pos = self.user_box.get_rect()
        self.user_box_pos.left = left
        self.user_box_pos.top = top
        screenObj.blit(self.user_box, self.user_box_pos)

    # renders list of users in users box, returns tup of user text/ rect
    def display_items(self, items, screenObj):
        user_names = []
        user_pos = []
        for i, name in enumerate(items):
            user_text = user_font.render(name, True, (10, 10, 10) )
            user_text_pos = user_text.get_rect()
            user_text_pos.left = (user_box_pos.left + 5)
            user_text_pos.top = user_box_pos.top + (i * (user_text_pos.height) + 2 )
            user_names.append(user_text)
            user_pos.append(user_text_pos)
            
        user_tups = zip(user_names, user_pos)
        for a, b in user_tups:      
            screenObj.blit(a, b)
        
        return user_tups

