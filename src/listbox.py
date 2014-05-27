#!/usr/bin/python2.7

import pygame


class ListBox():
    # screenObj - which surface to draw onto
    # colortup  - color to fill box. ex: (255,255,255)
    # x & y     - coordinates to draw the box at
    # height & width - dimensions of the rect
    def __init__(self, screenObj, colortup, width, height, left, top):
        "Make a box to display text items, such as usernames or actiive games."
        self.box_surface = pygame.Surface((width, height))
        self.box_surface.fill(colortup)
        self.box_surface_pos = self.box_surface.get_rect()
        self.box_surface_pos.left = left
        self.box_surface_pos.top = top
        screenObj.blit(self.box_surface, self.box_surface_pos)

    # renders list of users in users box, returns tup of user text/ rect
    def display_items(self, items, screenObj):
        list_box_font  = pygame.font.SysFont(None, 24)

        item_names = []
        item_pos = []

        for i, name in enumerate(items):
            item_text = list_box_font.render(name, True, (10, 10, 10) )
            item_text_pos = item_text.get_rect()
            item_text_pos.left = (self.box_surface_pos.left + 5)
            item_text_pos.top = self.box_surface_pos.top + (i * (item_text_pos.height) + 2 )
            item_names.append(item_text)
            item_pos.append(item_text_pos)
            
        item_tups = zip(item_names, item_pos)
        for a, b in item_tups:      
            screenObj.blit(a, b)
        
        return item_tups

