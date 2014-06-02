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
    def __init__(self, maker, name, limit=4):
        self.users      = []
        self.level_list = [0, 0, 0, 0]
        self.name       = name
        self.limit      = limit
        self.waiting    = True   # don't start the game yet
        self.add_user(maker)

    def add_user(self, user):
        user.game = self        # update user's game
        self.users.append(user) # add user to this game

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
            user.game = None

    def usernames(self):
        return [user.name for user in self.users]

    # check if any of the players won the game
    def check_winner(self):
        for i in level_list:
            if i == 10:
                return i
        return None

    def compact(self):
        return (self.name, id(self), len(self.users), self.limit)


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
        self.user_sockets  = {}

        # keep a collection of current games
        self.games         = []

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
        cmd, name = msg
        usernames = [u.name for u in self.users() if u.name]
        if cmd == "login" and name not in usernames:
            user.name  = name
            user.send(("login_result", True))
            user.send(("games", [g.compact() for g in self.games]))
            self.users_changed = True
        else:
            user.send(("login_result", False))

    def in_lobby(self, user, msg):
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
                        self.games_changed = True
                    break
        elif cmd == "chat":
            chat_msg = "{}: {}".format(user.name, msg[1]) # append who said it
            print "{} said {}".format(user.name, msg[1])
            for u in self.users():
                u.send(("chat", chat_msg))

    def in_game_waiting(self, user, msg):
        cmd = msg[0]
        if cmd == "user_num_update":
            self.user.send( ( "user_num_reply", [self.game.game_id, len(self.game.users)] ) )
        elif cmd == "send_words":
            self.user.send( ( "words_reply",  word_list) )
        elif cmd == "start_game":
            self.user.send( ( "start_game", [self.game_id, self.user.usernames]) )

        # will update users on current number of joined users
        # will end when sending a start game message to all users
        #
        # send a start message as: ("start_game", ["username1", "username2", ...])
        #
        # also need to send the word list to all players at game start..


    def in_game(self, user, msg):
        # will pass messages between users when updates occur
        # will end when one user finishes all words in wordlist
        # when ends, state for all users in game becomes lobby and game
        #   should be destroyed

        cmd = msg[0]
        # gameupdate: ("gameupdate, game_id, user_idx, [1, 2, 3, 4]")
        if cmd == "game_update_out":
            # increment the list at index user_idx
            self.user.game.level_list[user_idx] += 1
            # check if anyone won
            winner = self.user.game.check_winner()
            self.user.send( ( "game_update_in",
                              msg[1],
                              self.user.game.level_list) )
            if winner != None:
                self.user.send( ( "player_won", msg[1], winner ) )
        elif cmd == "end_game":
            # how can itrigger state change in program
            self.user.send( ( "end_game", game_id ) )


    def users(self):
        return self.user_sockets.itervalues()

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
            self.user_sockets[new_conn] = User(new_conn)
        else:
            try:
                msg = messenger.recv(conn)
                print "<got '{}'>".format(msg)
                self.user_sockets[conn].inbox.append(msg)
            except messenger.ClosedConnection:
                self._close(conn)

    def _send(self, conn):
        msg = self.user_sockets[conn].outbox.popleft()
        print "<sending '{}'>".format(msg)
        messenger.send(conn, msg)

    def _close(self, conn):
        print "<closing connection>"
        user = self.user_sockets[conn]
        if user.game:
            user.game.remove_user(user)
        del self.user_sockets[conn]
        conn.close()
        self.users_changed = True
