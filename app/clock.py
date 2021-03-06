# File:         clock.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse

# Assignment:   Final Project

# Description:
# The Clock provides system ticks to an event handler using the specialized
# post_tick() event generation.
#
# The clock uses a pygame clock object to regulate ticks at a framerate
# specified by the class label FRAMERATE (frames per second).

# third party modules
import pygame

# our modules
import base
import events


class Clock(base.Listener):
    FRAMERATE = 30

    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.running = True

    def run(self):
        '''While running, tick the clock, then post a tick to the event manager.
        '''
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(Clock.FRAMERATE)
            self.handler.post_tick()

    def notify(self, event):
        if isinstance(event, events.Stop):
            self.running = False
