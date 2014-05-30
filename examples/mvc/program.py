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

class Program(base.Controller):
    def __init__(self, handler):
        base.Controller.__init__(self, handler)
        self.user  = user.User(self.handler)
        self.game  = game.Game(self.handler)

    def notify(self, event):
        post_event = {
            events.UserLoggedIn:  events.LobbyView,
            events.UserLoggedOut: events.LoginView
        }.get(type(event), None)

        if post_event:
            self.handler.post_event(post_event())


class ViewSelector(base.Controller):
    def __init__(self, handler):
        base.Controller.__init__(self, handler)
        self.handler.register_for_ticks(self)

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('432 game')

        self.background = pygame.Surface(self.window.get_size())

        # inject self as handler so we can deliver messages only when we want
        self.views = {
            LOGIN: login.LoginView(self, self.background),
            LOBBY: lobby.LobbyView(self, self.background),
            GAME:  game.GameView(self, self.background)
        }
        self.state = LOGIN

    def notify(self, event):
        self.state = {
            events.LoginView: LOGIN,
            events.LobbyView: LOBBY,
            events.GameView:  GAME
        }.get(type(event), self.state)

        self.views[self.state].notify(event)

    def post_event(self, event):
        self.handler.post_event(event)

    def register_for_events(self, _):
        pass

    def tick(self):
        view = self.views[self.state]
        view.draw()
        view.window.blit(view.background, view.background.get_rect())
        self.window.blit(self.background, self.background.get_rect())
        pygame.display.flip()


def main():
    handler       = base.EventManager()
    inputs        = userinput.Input(handler)
    program_views = ViewSelector(handler)
    program       = Program(handler)

    clock.Clock(handler).run()


if __name__ == '__main__':
    main()
