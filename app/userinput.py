
import pygame

import base
import events


class Input(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.handler.register_for_ticks(self)

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handler.post_event(events.Stop())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.handler.post_event(events.Stop())
                else:
                    self.handler.post_event(events.KeyPress(event.key))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handler.post_event(events.MouseClick(pos))
