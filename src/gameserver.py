#!/usr/bin/python2.7

import collections
import select
import socket

# our libs
import message

LISTEN_QUEUE = 5
PORT         = 7307

class Game(object):
    def __init__(self, name, size):
        self.users = []
        self.name = name
        self.size = size

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


class UserServer(object):
    def __init__(self):
        # set up non-blocking server socket with reuse option
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('',PORT))
        self.server.listen(LISTEN_QUEUE)

        # map socket fds to User objects
        self._users = {}

    def users(self):
        return self._users.itervalues()

    def update(self):
        """Send and receive to and from any server sockets.
        """
        recv_list = [u.conn for u in self.users()]
        recv_list.append(self.server)
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

    def _recv(self, conn):
        if conn is self.server:
            new_conn, addr = self.server.accept()
            new_conn.setblocking(0)
            self._users[new_conn] = User(new_conn)
        else:
            try:
                data = message.recv(conn) # what if we want more than 1024?
                print "<got '{}'>".format(data)
                self._users[conn].inbox.append(data)
            except message.ClosedConnection:
                self._close(conn)

    def _send(self, conn):
        response = self._users[conn].outbox.popleft()
        print "<sending '{}'>".format(response)
        message.send(conn, response)

    def _close(self, conn):
        print "<closing connection>"
        user = self._users[conn]
        if user.game:
            user.game.remove_user(user)
        del self._users[conn]
        conn.close()


class GameServer(object):
    def __init__(self):
        self.server    = UserServer()
        self.games     = []
        self.usernames = []

    def register(self, user, msg):
        cmd, name = msg
        if cmd == "login" and name not in self.usernames:
            user.name  = name
            user.send(True)
        else:
            user.send(False)

    def in_lobby(self, user, msg):
        cmd = msg[0]
        if cmd == "users":
            user.send(self.usernames)
        elif cmd == "games":
            user.send([game.compact() for game in self.games])
        elif cmd == "create":
            new_game = Game(msg[1], 4)
            new_game.add_user(user)
            self.games.append(new_game)
            user.send(new_game.compact())
        elif cmd == "join":
            game_id = msg[1]
            for game in self.games:
                if id(game) == game_id and len(game.users) < game.size:
                    game.add_user(user)
                    user.send(game.compact())
                    break
            else:
                user.send(False)
        else:
            user.send(False)

    def in_game(self, user, msg):
        game = user.game
        cmd = msg[0]
        if cmd == "users":
            user.send(game.usernames())
        elif cmd == "exit":
            game.remove_user(user)
            user.send(True)
        else:
            user.send(False)

    def serve_forever(self):
        while True:
            self.server.update()

            # clean up games
            self.games = filter(lambda game: len(game.users) > 0, self.games)

            # get list of usernames
            self.usernames = [
                user.name for user in self.server.users() if user.name
            ]

            # handle requests
            for user in self.server.users():
                while user.has_messages():
                    msg = user.recv()
                    if user.name is None:
                        self.register(user, msg)
                    elif user.game is None:
                        self.in_lobby(user, msg)
                    else:
                        self.in_game(user, msg)
