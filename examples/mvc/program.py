#!/usr/bin/python2.7

import pygame

import base
import clock
import events
import game
import userinput
import lobby
import login
import user

LOGIN = 1
LOBBY = 2
GAME  = 3

class Program(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.handler.register_for_ticks(self)

        pygame.init()
        pygame.font.init()
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("firestarter")

        self.user = user.User(self.handler)

        self.modules = {
            LOGIN: login.Login(self.handler),
            LOBBY: lobby.Lobby(self.handler)
        }
        self.state = LOGIN

        self.handler.unregister_for_events(self.modules[LOBBY])

    def notify(self, event):
        if self.state == LOGIN:
            if isinstance(event, events.UserLoggedIn):
                self.change_state(LOBBY)
        elif self.state == LOBBY:
            if isinstance(event, events.UserLoggedOut):
                self.change_state_(LOGIN)

    def change_state(self, new_state):
        current_module = self.modules[self.state]
        self.handler.unregister_for_events(current_module)
        self.state = new_state
        new_module = self.modules[self.state]
        self.handler.register_for_events(new_module)

    def tick(self):
        self.modules[self.state].update()
        pygame.display.flip()


def main():
    handler = events.EventManager()
    inputs  = userinput.Input(handler)
    program = Program(handler)

    clock.Clock(handler).run()


if __name__ == '__main__':
    main()
