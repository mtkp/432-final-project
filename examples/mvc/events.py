# program/game events

class Event(object):
    '''Event base class.
    '''
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

class Logout(Event):
    pass

class UserLoggedIn(Event):
    pass

class UserLoggedOut(Event):
    pass

class GetUser(Event):
    pass

class GetUsers(Event):
    pass

class GetGames(Event):
    pass

class UserUpdate(Event):
    def __init__(self, user):
        self.user = user
