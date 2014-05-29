
import pygame

import base
import events


class Input(base.Controller):
    def __init__(self, handler):
        base.Controller.__init__(self, handler)
        self.handler.register_tick(self)

    def tick(self):
        for event in pygame.event.get():
            post_event = {
                pygame.QUIT: events.Stop,
                pygame.KEYDOWN: events.KeyPress,
                pygame.MOUSEBUTTONDOWN: events.MouseClick
            }.get(event.type, None)

            if post_event:
                self.handler.post_event(post_event())
