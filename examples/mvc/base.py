
import pygame


class EventObserver(object):
    def __init__(self, handler):
        self.handler = handler
        self.handler.register_event(self)

    def notify(self, event):
        """Handler calls this function to notify this observer.
        """
        pass


# M
class Model(EventObserver):
    def __init__(self, handler):
        EventObserver.__init__(self, handler)


# V
class View(EventObserver):
    def __init__(self, handler, window):
        EventObserver.__init__(self, handler)
        self.window = window
        self.background = pygame.Surface(self.window.get_size())
        self.font = pygame.font.SysFont("monospace", 24)

    def draw(self):
        """View selector calls this view to draw it.
        """
        pass


# C
class Controller(EventObserver):
    def __init__(self, handler):
        EventObserver.__init__(self, handler)
