#!/usr/bin/python2.7

import .

class Event(object):
    pass

class TickEvent(Event):
    pass

class StopEvent(Event):
    pass

class KeyPressEvent(Event):
    def __init__(self, key):
        self.key = key

class LoginViewEvent(Event):
    pass

class LobbyViewEvent(Event):
    pass

class GameViewEvent(Event):
    pass

class TryLoginEvent(Event):
    pass

class UserLoggedInEvent(Event):
    pass

class UserLoggedOutEvent(Event):
    pass

class EventHandler(object):
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        print "registering " + str(listener.__class__)
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)


class ControllerBase(object):
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.event_handler.register(self)


class Clock(ControllerBase):
    def __init__(self, event_handler):
        ControllerBase.__init__(self, event_handler)
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(30)
            self.event_handler.post(TickEvent())

    def notify(self, event):
        if isinstance(event, StopEvent):
            self.running = False


class Keyboard(ControllerBase):
    def __init__(self, event_handler):
        ControllerBase.__init__(self, event_handler)

    def notify(self, event):
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_handler.post(StopEvent())
                elif event.type == pygame.KEYDOWN:
                    self.event_handler.post(KeyPressEvent(event.key))


class ProgramController(ControllerBase):
    def __init__(self, event_handler):
        ControllerBase.__init__(self, event_handler)

    def notify(self, event):
        {UserLoggedInEvent:  self.event_handler.post(LobbyViewEvent()),
         UserLoggedOutEvent: self.event_handler.post(LoginViewEvent())
        }.get(type(event))


class ViewBase(object):
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.event_handler.register(self)

    def notify(self, event):
        pass

    def draw(self):
        pass


class LoginView(ViewBase):
    def __init__(self, event_handler, window):
        ViewBase.__init__(self, event_handler)
        self.window = window
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill(color.Red)
        self.font = pygame.font.SysFont("monospace", 24)

    def notify(self, event):
        pass

    def draw(self):
        self.background.blit(
            self.font.render(str(type(self)), 1, color.Black),
            self.background.get_rect()
        )
        self.window.blit(self.background, self.background.get_rect())


class LobbyView(ViewBase):
    def __init__(self, event_handler, window):
        ViewBase.__init__(self, event_handler)
        self.window = window
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill(color.Green)
        self.font = pygame.font.SysFont("monospace", 24)

    def notify(self, event):
        pass

    def draw(self):
        self.background.blit(
            self.font.render(str(type(self)), 1, color.Black),
            self.background.get_rect()
        )
        self.window.blit(self.background, self.background.get_rect())


class GameView(ViewBase):
    def __init__(self, event_handler, window):
        ViewBase.__init__(self, event_handler)
        self.window = window
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill(color.Blue)
        self.font = pygame.font.SysFont("monospace", 24)

    def notify(self, event):
        pass

    def draw(self):
        self.background.blit(
            self.font.render(str(type(self)), 1, color.Black),
            self.background.get_rect()
        )
        self.window.blit(self.background, self.background.get_rect())


class ViewController(ControllerBase):
    def __init__(self, event_handler):
        ControllerBase.__init__(self, event_handler)

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('432 game')

        self.background = pygame.Surface(self.window.get_size())

        self.views = {
            "login": LoginView(self.event_handler, self.background),
            "lobby": LobbyView(self.event_handler, self.background),
            "game":  GameView(self.event_handler, self.background)
        }
        self.state = "login"


    def notify(self, event):
        if isinstance(event, TickEvent):
            self.draw()
        else:
            self.state = {
                LoginViewEvent: "login",
                LobbyViewEvent: "lobby",
                GameViewEvent:  "game"
            }.get(type(event), self.state)


    def draw(self):
        self.views[self.state].draw()
        self.window.blit(self.background, self.background.get_rect())
        pygame.display.flip()


class ModelBase(object):
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.event_handler.register(self)

    def notify(self, event):
        pass


class UserModel(ModelBase):
    def __init__(self, event_handler):
        ModelBase.__init__(self, event_handler)

    def notify(self, event):
        if isinstance(event, TryLoginEvent):
            name = TryLoginEvent()



def main():
    event_handler = EventHandler()

    clock = Clock(event_handler)
    keyboard = Keyboard(event_handler)
    view = ViewController(event_handler)
    controller = ProgramController(event_handler)
    user = UserModel(event_handler)

    clock.run()


if __name__ == '__main__':
    main()
