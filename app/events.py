# File:         events.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse

# Assignment:   Final Project

# Description:
# Event objects are generated and examined by various members of an
# EventManager. Events are very simple, providing only a name and occasionally
# a few special fields for special communication.


class Event(object):
    '''Event base class.
    '''
    pass

class Stop(Event):
    '''Stop the program.
    '''
    pass

class KeyPress(Event):
    '''A keyboard key press event. Contains the ascii code.
    '''
    def __init__(self, key):
        self.key = key

class MouseClick(Event):
    '''A mouse click event. Contains the x-y coordinates of that mouse click.
    '''
    def __init__(self, pos):
        self.pos = pos

class LoginError(Event):
    '''Generated when login fails.
    '''
    def __init__(self, msg):
        self.msg = msg

class TryLogin(Event):
    '''Request to the NetworkManager to try to login to the server with the
    given name.
    '''
    def __init__(self, name, server):
        self.name = name
        self.server = server

class TryCreateGame(Event):
    '''Try to create a game with the specified name.
    '''
    def __init__(self, name):
        self.name = name

class TryJoinGame(Event):
    '''Try to join a game using the game id.
    '''
    def __init__(self, game_id):
        self.game_id = game_id

class JoinGame(Event):
    '''Generated when a game is successfully joined (per the server).
    '''
    def __init__(self, game_name, game_users):
        self.game_name = game_name
        self.game_users = game_users

class TrySendChat(Event):
    '''Try to send a chat message to the server.
    '''
    def __init__(self, msg):
        self.msg = msg

class LeaveGame(Event):
    '''Exit an in-progress game.
    '''
    pass

class Logout(Event):
    '''Logout of the server.
    '''
    pass

class UserLoggedIn(Event):
    '''User successfully logged in.
    '''
    pass

class UserLoggedOut(Event):
    '''User successfully logged out.
    '''
    pass

class UserJoinedGame(Event):
    '''User successfully joined a game.
    '''
    pass

class GameStarted(Event):
    '''GameStarted indicates that the game play has begun per the server.
    '''
    pass

class ModelUpdated(Event):
    '''ModelUpdated notifies any listening events that the program model
    has changed. See the model object in program.py.
    - Username
    - Users list
    - Games list
    - Chat log
    '''
    pass

class GameInitialize(Event):
    '''Holds and transfers the initialized game.
    '''
    def __init__(self, words, user_names):
        self.words = words
        self.user_names = user_names

class GameUpdateOut(Event):
    '''Send an in-game update to the server, by way of the network manager.
    '''
    def __init__(self, user_name):
        self.user_name = user_name

class GameUpdateIn(Event):
    '''Generated by the network manager on receiving game updates from the
    server.
    '''
    def __init__(self, level_list):
        self.level_list = level_list

class StartGame(Event):
    '''This event actually changes the program state to GAME.
    '''
    pass

class EndGame(Event):
    '''Indicates a game has ended, return to lobby.
    '''
    pass

class PlayerWon(Event):
    '''Indicates a winner of the game has been determined, so stop game play.
    '''
    def __init__(self, msg):
        self.msg = msg

