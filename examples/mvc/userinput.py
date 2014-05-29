
import pygame

import base
import events


class Input(base.Controller):
    def __init__(self, handler):
        base.Controller.__init__(self, handler)
        self.handler.register_for_ticks(self)

    def tick(self):
        for event in pygame.event.get():
            event_generator = {
                pygame.QUIT: self.post_stop,
                pygame.KEYDOWN: self.post_key_press,
                pygame.MOUSEBUTTONDOWN: self.post_mouse_click
            }.get(event.type, None)

            if event_generator:
                self.handler.post_event(event_generator(event))

    def post_stop(self, event):
        return events.Stop()

    def post_mouse_click(self, event):
        mouse_pos = pygame.mouse.get_pos()
        return events.MouseClick(mouse_pos)

    def post_key_press(self, event):
        return events.KeyPress(event.key)

