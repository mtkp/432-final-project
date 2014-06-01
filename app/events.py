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

class StartGame(Event):
    pass

class EndGame(Event):
    pass

# player got a word right, needs to be moved locally and remotely
class PlayerMoved(Event):
    pass

# player won the game, notify server to end the game
class PlayerWon(Event):
    pass

# opponent got a word right, needs to be moved locally
class OpponentMoved(Event):
    pass

# Opponent wins the game
class OpponentWon(Event):
    def __init__(self, opponent):
        self.opponent = opponent

# Opponent leaves unexpectedly, like quit during game or connection lost
class OpponentGone(Event):
    pass


class EventManager(object):
    def __init__(self):
        import collections
        self.event_listeners = []
        self.tick_listeners  = []
        self.event_queue     = collections.deque()
        self.register_for_ticks(self)

    def register_for_events(self, listener):
        print "registering for events " + str(listener.__class__)
        self.event_listeners.append(listener)

    def unregister_for_events(self, listener):
        if listener in self.event_listeners:
            self.event_listeners.remove(listener)

    def register_for_ticks(self, listener):
        print "registering for ticks " + str(listener.__class__)
        self.tick_listeners.append(listener)

    def post_event(self, event):
        self.event_queue.append(event)

    def post_tick(self):
        for listener in self.tick_listeners:
            listener.tick()

    def tick(self):
        while len(self.event_queue) > 0:
            event = self.event_queue.popleft()
            for listener in self.event_listeners:
                listener.notify(event)
