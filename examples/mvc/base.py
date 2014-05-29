
import collections

import pygame


class EventManager(object):
    def __init__(self):
        self.event_listeners = []
        self.tick_listeners  = [self]
        self.event_queue     = collections.deque()

    def register_for_events(self, listener):
        print "registering for events " + str(listener.__class__)
        self.event_listeners.append(listener)

    def register_for_ticks(self, listener):
        print "registering for ticks " + str(listener.__class__)
        self.tick_listeners.append(listener)

    def post_event(self, event):
        self.event_queue.append(event)

    def post_tick(self):
        for listener in self.tick_listeners:
            listener.tick()

    def tick(self):
        while len(self.event_queue) > 0:
            event = self.event_queue.popleft()
            for listener in self.event_listeners:
                listener.notify(event)


class EventListener(object):
    def __init__(self, handler):
        self.handler = handler
        self.handler.register_for_events(self)

    def notify(self, event):
        """EventManager calls this function to notify this listener.
        """
        pass


# M
class Model(EventListener):
    def __init__(self, handler):
        EventListener.__init__(self, handler)


# V
class View(EventListener):
    def __init__(self, handler, window):
        EventListener.__init__(self, handler)
        self.window = window
        self.background = pygame.Surface(self.window.get_size())
        self.font = pygame.font.SysFont("monospace", 20)

    def draw(self):
        """View selector calls this view to draw it.
        """
        pass


# C
class Controller(EventListener):
    def __init__(self, handler):
        EventListener.__init__(self, handler)
