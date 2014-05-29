
class Event(object):
    pass

class Stop(Event):
    pass

class KeyPress(Event):
    def __init__(self, key):
        self.key = key

class MouseClick(Event):
    def __init__(self, pos):
        self.pos = pos

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

class GetUsers(Event):
    pass

class Users(Event):
    def __init__(self, users):
        self.users = users

