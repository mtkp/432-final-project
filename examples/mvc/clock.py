
import pygame

import base
import events


class Clock(base.Controller):
    FRAMERATE = 30

    def __init__(self, handler):
        base.Controller.__init__(self, handler)
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(Clock.FRAMERATE)
            self.handler.post_tick()

    def notify(self, event):
        if isinstance(event, events.Stop):
            self.running = False
