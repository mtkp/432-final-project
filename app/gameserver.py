#!/usr/bin/python2.7

# python libs
import collections
import select
import socket

# our libs
import messenger

LISTEN_QUEUE = 5
PORT         = 7307

class Game(object):
    def __init__(self, name, size):
        self.users   = []
        self.name    = name
        self.size    = size
        self.waiting = True   # don't start the game yet

    def add_user(self, user):
        user.game = self
        self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
            user.game = None

    def usernames(self):
        return [user.name for user in self.users]

    def compact(self):
        return (self.name, id(self), self.usernames(), self.size)


class User(object):
    def __init__(self, conn):
        self.conn   = conn
        self.inbox  = collections.deque()
        self.outbox = collections.deque()
        self.name   = None
        self.game   = None

    def has_messages(self):
        return len(self.inbox) > 0

    def recv(self):
        return self.inbox.popleft()

    def send(self, msg):
        self.outbox.append(msg)

class GameServer(object):
    def __init__(self):
        # set up non-blocking server socket with reuse option
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(0)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('',PORT))
        self.server_socket.listen(LISTEN_QUEUE)

        # map socket fds to User objects
        self._users        = {}
        self.games         = []
        self.usernames     = []
        self.users_changed = False

    def serve_forever(self):
        while True:
            self.update()

            # clean up games
            self.games = filter(lambda game: len(game.users) > 0, self.games)

            # get list of usernames
            self.usernames = [
                user.name for user in self.users() if user.name
            ]

            # notify users if user list changed
            if self.users_changed:
                for user in self.users():
                    user.send(("users", self.usernames))
            self.users_changed = False

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

    # -- handle user requests, per the user state --
    # - regsiter
    # - in_lobby
    # - in_game_waiting
    # - in_game

    def register(self, user, msg):
        cmd, name = msg
        if cmd == "login" and name not in self.usernames:
            user.name  = name
            user.send(("login_result", True))
            self.users_changed = True
        else:
            user.send(("login_result", False))

    def in_lobby(self, user, msg):
        cmd = msg[0]
        if cmd == "create_game":
            pass

    def in_game_waiting(self, user, msg):
        # will update users on current number of joined users
        # probably also a good time to send out the word list...?
        # will end when sending a start game message to all users
        pass

    def in_game(self, user, msg):
        # will pass messages between users when updates occur
        # will end when one user finishes all words in wordlist
        # when ends, state for all users in game becomes lobby and game
        #   should be destroyed
        #
        # case send upate:
        #     self.user.send( ( "game_update", [5, 7, 8, 3] ) )
        pass

    def users(self):
        return self._users.itervalues()

    def update(self):
        """Actually send and receive to and from any server_socket sockets,
        using select.
        """
        recv_list = [u.conn for u in self.users()]
        recv_list.append(self.server_socket)
        send_list = [u.conn for u in self.users() if len(u.outbox) > 0]

        recv_list, send_list, exception_list = \
            select.select(recv_list, send_list, recv_list)
        for conn in recv_list:
            self._recv(conn)
        for conn in send_list:
            self._send(conn)
        for conn in exception_list:
            print "<socket exception...>"
            self._close(conn)

    # -- private --

    def _recv(self, conn):
        if conn is self.server_socket:
            new_conn, addr = self.server_socket.accept()
            new_conn.setblocking(0)
            self._users[new_conn] = User(new_conn)
        else:
            try:
                msg = messenger.recv(conn)
                print "<got '{}'>".format(msg)
                self._users[conn].inbox.append(msg)
            except messenger.ClosedConnection:
                self._close(conn)

    def _send(self, conn):
        msg = self._users[conn].outbox.popleft()
        print "<sending '{}'>".format(msg)
        messenger.send(conn, msg)

    def _close(self, conn):
        print "<closing connection>"
        user = self._users[conn]
        if user.game:
            user.game.remove_user(user)
        del self._users[conn]
        conn.close()
        self.users_changed = True
