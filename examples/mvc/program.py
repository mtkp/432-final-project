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


class Program(base.Controller):
    def __init__(self, handler):
        base.Controller.__init__(self, handler)
        self.user = user.User(self.handler)
        self.game = game.Game(self.handler)

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
        self.handler.register_tick(self)

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('432 game')

        self.background = pygame.Surface(self.window.get_size())

        self.views = {
            "login": login.LoginView(self.handler, self.background),
            "lobby": lobby.LobbyView(self.handler, self.background),
            "game":  game.GameView(self.handler, self.background)
        }
        self.state = "login"

    def notify(self, event):
        self.state = {
            events.LoginView: "login",
            events.LobbyView: "lobby",
            events.GameView:  "game"
        }.get(type(event), self.state)

    def tick(self):
        self.views[self.state].draw()
        self.window.blit(self.background, self.background.get_rect())
        pygame.display.flip()


def main():
    handler = events.Handler()

    draw_clock = clock.Clock(handler)
    inputs     = userinput.Input(handler)

    program_views = ViewSelector(handler)
    program       = Program(handler)

    draw_clock.run()

if __name__ == '__main__':
    main()
