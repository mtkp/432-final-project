#!/usr/bin/python2.7

import pygame

import base
import clock
import events
import game
import lobby
import login
import netmanagerhigh
import start
import userinput
import gamewait

START    = 0
LOGIN    = 1
LOBBY    = 2
GAMEWAIT = 3
GAME     = 4


class Program(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.handler.register_for_ticks(self)

        pygame.init()
        pygame.font.init()
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("type it")

        self.net_manager_high = netmanagerhigh.NetManagerHigh(self.handler)

        self.modules = {
            START:    start.Start(self.handler),
            LOGIN:    login.Login(self.handler),
            LOBBY:    lobby.Lobby(self.handler),
            GAMEWAIT: gamewait.GameWait(self.handler),
            GAME:     game.Game(self.handler)
        }

        # set current state
        # self.state = GAME   # GREG
        self.state = START  # MATT
        self.handler.register_for_events(self.modules[self.state])

    def notify(self, event):
        if self.state == START:
            if isinstance(event, events.MouseClick):
                self.change_state(LOGIN)
        if self.state == LOGIN:
            if isinstance(event, events.UserLoggedIn):
                self.change_state(LOBBY)
        elif self.state == LOBBY:
            if isinstance(event, events.UserLoggedOut):
                self.change_state(LOGIN)
            elif isinstance(event, events.UserJoinedGame):
                self.change_state(GAMEWAIT)
        elif self.state == GAMEWAIT:
            if isinstance(event, events.LeaveGame):
                self.change_state(LOBBY)
            elif isinstance(event, events.UserGameStarted):
                self.change_state(GAME)
        elif self.state == GAME:
            if isinstance(even, events.UserGameEnded):
                self.change_state(LOBBY)


    def change_state(self, new_state):
        current_module = self.modules[self.state]
        self.handler.unregister_for_events(current_module)
        self.state = new_state
        new_module = self.modules[self.state]
        self.handler.register_for_events(new_module)
        self.handler.post_event(events.UserUpdate(self.net_manager_high))

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
