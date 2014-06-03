
#

# File:         .py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:

import pygame

import color


class Listener(object):
    """Listener automatically registers with handler.
    """
    def __init__(self, handler):
        self.handler = handler
        self.handler.register_for_events(self)

    def notify(self, event):
        """EventManager calls this function to notify this listener.
        """
        pass


class Module(object):
    """Module does not automatically register with handle.
    """
    def __init__(self, handler, model):
        self.handler = handler
        self.model = model
        self.window = pygame.display.get_surface()
        self.width, self.height = self.window.get_size()
        self.background_color = color.Gray
        self.background = pygame.Surface(self.window.get_size())
        self.font = pygame.font.SysFont("monospace", 20)
        self.draw_set = []

    def reload(self):
        pass

    def notify(self, event):
        """EventManager calls this function to notify this listener.
        """
        pass

    def draw(self):
        """Draws all objects in view draw set.
        """
        self.background.fill(self.background_color)
        map(lambda i: i.draw(), self.draw_set)
        self.window.blit(self.background, self.background.get_rect())

