
import pygame

import color


class Listener(object):
    def __init__(self, handler):
        self.handler = handler
        self.handler.register_for_events(self)

    def notify(self, event):
        """EventManager calls this function to notify this listener.
        """
        pass


class Module(Listener):
    def __init__(self, handler):
        Listener.__init__(self, handler)
        self.window = pygame.display.get_surface()
        self.width, self.height = self.window.get_size()
        self.background_color = color.Gray
        self.background = pygame.Surface(self.window.get_size())
        self.font = pygame.font.SysFont("monospace", 20)
        self.draw_set = []

    def draw(self):
        """Draws all objects in view draw set.
        """
        self.background.fill(self.background_color)
        map(lambda i: i.draw(), self.draw_set)
        self.window.blit(self.background, self.background.get_rect())

