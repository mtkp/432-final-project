# File:         gameserver.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse

# Assignment:   Final Project

# Description:
# GameServer is a smart, centralized server implementation supporting the
# "type it" game.
#
# GameServer is implemented using raw TCP sockets, and python's "select"
# function, which provides an OS-agnostic way to poll system sockets.
#
# Sockets are non-blocking, with TCP_NODELAY to move messages as quickly as
# possible.
#
# For each user, the game server reads in any incoming messages, and handles
# that message using a state machine for that user. This greatly simplifies
# exceptional conditions and enables the user to ignore messages that do not
# fit the known state of the user according to the server.
#
# Certain events trigger server-initiated messages, such as changes to chat,
# user list, games list, and in-game events.


# python libs
import collections
import select
import socket
import random

# our libs
import messenger


LISTEN_QUEUE    = 5
PORT            = 7307
WORDS_FILE      = "text/min_8"
GAME_WORD_COUNT = 15


def get_random_words(all_words):
    '''Get random words from a list of words.
    '''
    real_word_list = []
    range_max = len(all_words) - 1
    for _ in xrange(GAME_WORD_COUNT):
        real_word_list.append(all_words[random.randint(0, range_max)])
    return real_word_list

def read_words(words_file=WORDS_FILE):
    '''Provides a random list of words from a given text file.
    '''
    all_words = [word for line in open(words_file, 'r') for word in line.split()]
    return get_random_words(all_words)


class Game(object):
    def __init__(self, maker, name, limit=4):
        '''Game objects contain all information relevent to the server
        for a currently active game.
        '''
        self.name       = name
        self.limit      = limit
        self.users      = []
        self.words      = read_words()
        self.level_list = [0, 0, 0, 0]
        self.waiting    = True # don't start the game yet
        self.add_user(maker)   # add the game maker to the game

    def add_user(self, user):
        user.game = self         # update user's game
        self.users.append(user)  # add user to this game

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
            user.game = None

    def remove_all_users(self):
        for user in self.users:
            user.game = None
        self.users = []

    def usernames(self):
        return [user.name for user in self.users]

    def get_index(self, user):
        for i, u in enumerate(self.users):
            if u == user:
                return i

    def check_winner(self):
        '''Check and get the winning player, if any players have won the game.
        '''
        for i, level in enumerate(self.level_list):
            if level == GAME_WORD_COUNT:
                return self.users[i]
        return None

    def compact(self):
        '''Package the game into a simple tuple representation to send to
        clients for displaying in the lobby view.
        '''
        return (self.name, id(self), len(self.users), self.limit)

    # wraps up the game's users names and word list to be sent out
    def initialize(self):
        '''Package the game into a simple tuple representaiton to send to
        clients who are about to start the game.
        '''
        return (self.words, self.usernames())


class User(object):
    def __init__(self, conn):
        self.conn = conn
        self.inbox = collections.deque()
        self.outbox = collections.deque()
        self.name = None
        self.game = None

    def has_messages(self):
        return len(self.inbox) > 0

    def recv(self):
        return self.inbox.popleft()

    def send(self, msg):
        self.outbox.append(msg)


class GameServer(object):
    def __init__(self):
        # set up a TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # as non-blocking
        self.server_socket.setblocking(0)

        # with reuse options (so we can quickly reboot server)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # with no Neagle's - so we can quickly write messages
        self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # bind to the "type it" port
        self.server_socket.bind(('',PORT))

        # set up the listen queue
        self.server_socket.listen(LISTEN_QUEUE)

        # map socket fds to User objects
        self.user_sockets = {}

        # keep a collection of current games and states
        self.games = []
        self.users_changed = False
        self.games_changed = False

    def serve_forever(self):
        while True:
            self.update()

            # clean up games
            for game in self.games:
                if len(game.users) == 0:
                    self.games_changed = True
            self.games = filter(lambda game: len(game.users) > 0, self.games)

            # listen and handle user requests
            for user in self.users():
                while user.has_messages():
                    msg = user.recv()
                    if user.name is None:
                        self.register(user, msg)
                    elif user.game is None:
                        self.in_lobby(user, msg)
                    elif user.game.waiting:
                        self.in_game_waiting(user, msg)
                    else:
                        self.in_game(user, msg)

            # notify users if user list changed
            if self.users_changed:
                usernames = [u.name for u in self.users() if u.name]
                for user in self.users():
                    user.send(("users", usernames))
                self.users_changed = False

            # notify users if games list changed
            if self.games_changed:
                all_games = [g.compact() for g in self.games]
                for user in self.users():
                    user.send(("games", all_games))
                self.games_changed = False

    # -- handle user requests, per the user state --
    # - regsiter
    # - in_lobby
    # - in_game_waiting
    # - in_game

    def register(self, user, msg):
        '''Users in registration state can only login.
        When a user updates, broadcast an updated username list to all users.
        '''
        cmd, name = msg
        usernames = [u.name for u in self.users() if u.name]
        if cmd == "login" and name not in usernames:
            user.name = name
            user.send(("login_result", True))
            user.send(("games", [g.compact() for g in self.games]))
            self.users_changed = True
        else:
            user.send(("login_result", False))

    def in_lobby(self, user, msg):
        '''Users in lobby state can create, and join games, and can also
        send chat messages.
        If a game is created or joined, broadcast an updated games list to
        all users.
        '''
        cmd = msg[0]
        if cmd == "create":
            game_name = msg[1]
            game = Game(user, game_name)
            self.games.append(game)
            user.send(("joined", game.compact()))
            self.games_changed = True
        elif cmd == "join":
            game_id = msg[1]
            for game in self.games:
                if id(game) == game_id:
                    if len(game.users) < game.limit:
                        game.add_user(user)
                        user.send(("joined", game.compact()))

                        # tell other waiting users to update player count
                        for usr in (u for u in game.users if u != user):
                            usr.send(("wait_update", game.compact()))

                        # start game if enough players
                        if len(game.users) == game.limit:
                            # game is ready to play!
                            for usr in game.users:
                                usr.send(("start_game", None))
                                usr.send((
                                    "game_initialize",
                                    game.initialize()
                                    ))
                            game.waiting = False
                        self.games_changed = True
                    break
        elif cmd == "chat":
            # prepend with username
            chat_msg = "{}: {}".format(user.name[:19], msg[1])
            for u in self.users():
                u.send(("chat", chat_msg))

    def in_game_waiting(self, user, msg):
        '''Users in game-waiting state are waiting for a game to begin.
        The only available action is exiting the game.
        '''
        game = user.game
        cmd = msg[0]
        if cmd == "exit_game":
            game.remove_user(user)
            for usr in game.users:
                usr.send(("wait_update", game.compact()))
            self.games_changed = True


    def in_game(self, user, msg):
        '''Users in the game state send game updates to the server. This is
        the only available action in this state. Upon receiving a game update
        message, the server increments the level for that user and broadcasts
        the updated level_list to all other users.
        '''
        cmd = msg[0]
        game = user.game
        if cmd == "game_update_out":
            user_index = game.get_index(user)
            game.level_list[user_index] += 1
            for usr in game.users:
                usr.send((
                    "game_update_in",
                    game.level_list
                    ))
            winner = game.check_winner()
            if winner is not None:
                for usr in game.users:
                    usr.send((
                        "player_won",
                        "{} wins!".format(winner.name)
                        ))
                game.remove_all_users()
                self.games_changed = True


    def users(self):
        return self.user_sockets.itervalues()

    def update(self):
        """*Actually* send and receive to and from any server_socket sockets,
        using select.
        """
        recv_list = [u.conn for u in self.users()]
        recv_list.append(self.server_socket)
        send_list = [u.conn for u in self.users() if len(u.outbox) > 0]

        recv_list, send_list, exception_list = \
            select.select(recv_list, send_list, recv_list, 0)
        for conn in recv_list:
            self._recv(conn)
        for conn in send_list:
            self._send(conn)
        for conn in exception_list:
            print "<socket exception...>"
            self._close(conn)

    # -- private --

    def _recv(self, conn):
        '''Read in any messages using Messenger, and add them to the user's
        inbox.
        '''
        if conn is self.server_socket:
            # add new connections to the server's client list
            new_conn, addr = self.server_socket.accept()

            # set socket to non-blocking
            new_conn.setblocking(0)

            # use TCP_NODELAY
            new_conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.user_sockets[new_conn] = User(new_conn)
        else:
            try:
                msg = messenger.recv(conn)
                print "<got '{}'>".format(msg)
                self.user_sockets[conn].inbox.append(msg)
            except messenger.ClosedConnection:
                self._close(conn)

    def _send(self, conn):
        '''Send any messages that are in the outbox.
        '''
        msg = self.user_sockets[conn].outbox.popleft()
        print "<sending '{}'>".format(msg)
        messenger.send(conn, msg)

    def _close(self, conn):
        '''When a connection is closed, close the socket, delete the user,
        and broadcast the updated user list to all remaining users.
        '''
        print "<closing connection>"
        user = self.user_sockets[conn]
        if user.game:
            user.game.remove_user(user)
        del self.user_sockets[conn]
        conn.close()
        self.users_changed = True
