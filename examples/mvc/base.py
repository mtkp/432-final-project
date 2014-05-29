
import pygame


class Handler(object):
    def __init__(self):
        self.event_listeners = []
        self.tick_listeners = []

    def register_event(self, listener):
        print "registering " + str(listener.__class__)
        self.event_listeners.append(listener)

    def register_tick(self, listener):
        self.tick_listeners.append(listener)

    def post_event(self, event):
        for listener in self.event_listeners:
            listener.notify(event)

    def post_tick(self):
        for listener in self.tick_listeners:
            listener.tick()


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
        self.font = pygame.font.SysFont("monospace", 20)

    def draw(self):
        """View selector calls this view to draw it.
        """
        pass


# C
class Controller(EventObserver):
    def __init__(self, handler):
        EventObserver.__init__(self, handler)
