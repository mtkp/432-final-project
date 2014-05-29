
class Event(object):
    pass

class Stop(Event):
    pass

class KeyPress(Event):
    pass

class MouseClick(Event):
    pass

class LoginView(Event):
    pass

class LoginError(Event):
    def __init__(self, msg):
        self.msg = msg

class LobbyView(Event):
    pass

class GameView(Event):
    pass

class TryLogin(Event):
    def __init__(self, name, server):
        self.name = name
        self.server = server

class UserLoggedIn(Event):
    pass

class UserLoggedOut(Event):
    pass


class Handler(object):
    def __init__(self):
        self.event_listeners = []
        self.tick_listeners = []

    def register_event(self, listener):
        print "registering " + str(listener.__class__)
        self.event_listeners.append(listener)

    def register_tick(self, listener):
        self.tick_listeners.append(listener)

    def post_event(self, event):
        for listener in self.event_listeners:
            listener.notify(event)

    def post_tick(self):
        for listener in self.tick_listeners:
            listener.tick()

