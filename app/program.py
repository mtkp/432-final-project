#!/usr/bin/python2.7

# File:         program.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:
# Operates the client side of the overall program, which uses the MVC model.
# Uses an event manager, keyboard/mouse input controller, and a clock. The 
# program transitions between different states, triggered by events from the
# event handler. Model maintains the state(data) across different states of 
# the program.  input controls input from devices like the keyboard and the 
# #mouse. clock contains the program's main game loop and controls framerate. 
# the program is operating on top of pygame, and game library for python.

# third party modules
import pygame

# our modules
import base
import clock
import eventmanager
import events
import game
import lobby
import login
import netmanager
import start
import userinput
import gamewait

class State:
    START    = 0
    LOGIN    = 1
    LOBBY    = 2
    GAMEWAIT = 3
    GAME     = 4

class Model(object):
    def __init__(self):
        self.setup()

    def setup(self):
        self.username     = None
        self.current_game = (0, 0, 0, 0)
        self.all_users    = []
        self.all_games    = []
        self.chat_log     = []


class Program(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.handler.register_for_ticks(self)

        pygame.init()
        pygame.font.init()
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("type it")

        self.model = Model()
        self.net   = netmanager.NetManager(self.handler, self.model)

        self.modules = {
            State.START:    start.Start(self.handler, self.model),
            State.LOGIN:    login.Login(self.handler, self.model),
            State.LOBBY:    lobby.Lobby(self.handler, self.model),
            State.GAMEWAIT: gamewait.GameWait(self.handler, self.model),
            State.GAME:     game.Game(self.handler, self.model)
        }

        # set current state
        self.state = State.START
        self.handler.register_for_events(self.modules[self.state])

    def notify(self, event):
        if self.state == State.START:
            if isinstance(event, events.MouseClick):
                self.change_state(State.LOGIN)
        if self.state == State.LOGIN:
            if isinstance(event, events.UserLoggedIn):
                self.change_state(State.LOBBY)
        elif self.state == State.LOBBY:
            if isinstance(event, events.UserLoggedOut):
                self.model.setup()
                self.change_state(State.LOGIN)
            elif isinstance(event, events.UserJoinedGame):
                self.change_state(State.GAMEWAIT)
        elif self.state == State.GAMEWAIT:
            if isinstance(event, events.LeaveGame):
                self.change_state(State.LOBBY)
            elif isinstance(event, events.StartGame):
                self.change_state(State.GAME)
        elif self.state == State.GAME:
            if isinstance(event, events.EndGame):
                self.change_state(State.LOBBY)

    def change_state(self, new_state):
        current_module = self.modules[self.state]
        self.handler.unregister_for_events(current_module)
        self.state = new_state
        new_module = self.modules[self.state]
        self.handler.register_for_events(new_module)
        new_module.reload()

    def tick(self):
        self.modules[self.state].draw()
        pygame.display.flip()


def main():
    handler  = eventmanager.EventManager()
    user_inp = userinput.Input(handler)
    program  = Program(handler)
    clock.Clock(handler).run()

if __name__ == '__main__':
    main()
