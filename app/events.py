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

class LoginError(Event):
    def __init__(self, msg):
        self.msg = msg

class TryLogin(Event):
    def __init__(self, name, server):
        self.name = name
        self.server = server

class TryCreateGame(Event):
    def __init__(self, name):
        self.name = name

class TryJoinGame(Event):
    def __init__(self, game_id):
        self.game_id = game_id

class JoinGame(Event):
    def __init__(self, game_name, game_users):
        self.game_name = game_name
        self.game_users = game_users

class TrySendChat(Event):
    def __init__(self, msg):
        self.msg = msg

class LeaveGame(Event):
    pass

class Logout(Event):
    pass

class UserLoggedIn(Event):
    pass

class UserLoggedOut(Event):
    pass

class UserJoinedGame(Event):
    pass

# trigger state change from wait to game
class GameStarted(Event):
    pass

class ModelUpdated(Event):
    pass

# in game state, send the game a copy of word list and user list
class GameInitialize(Event):
    def __init__(self, words, user_names):
        self.words = words
        self.user_names = user_names

# game update from client to server
class GameUpdateOut(Event):
    def __init__(self, user_name):
        self.user_name = user_name

# recieve a game update from the server
class GameUpdateIn(Event):
    def __init__(self, level_list):
        self.level_list = level_list

# state change from wait to to game when user limit is reached
class StartGame(Event):
    pass

class EndGame(Event):
    pass

# player won the game, from server
class PlayerWon(Event):
    def __init__(self, msg):
        self.msg = msg

class EventManager(object):
    def __init__(self):
        import collections
        self.event_listeners = []
        self.tick_listeners = []
        self.event_queue = collections.deque()
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
