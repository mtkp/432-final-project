#!/usr/bin/python2.7
# netmanagerlow.py

# python libs
import socket
import select
import collections

# our libs
import gameserver
import messenger

class InvalidFormat(Exception):
    """The given username formatting is invalid."""
    pass

class UsernameUnavailable(Exception):
    """The server rejected the username."""
    pass

class ServerNotFound(Exception):
    """Unable to connect to the given server."""
    pass

class NetManagerLow(object):
    def __init__(self):
        self.outbox = collections.deque()
        self.inbox  = collections.deque()
        self.conn   = None

    # we should probably rename this since it no longer *only* gets messages
    def update(self):
        """Get the next message from the TCP buffer if available, and add
        to inbox.
        Send the next message in the outbox if it is not empty.
        """
        recv_list, send_list, error_list = \
            select.select([self.conn], [self.conn], [self.conn])

        # for each of those port we want to send out on, send
        for i in send_list:
            if len(self.outbox) > 0:
                messenger.send(i, self.outbox.popleft())
        # for each port we want to receive on, print data received
        for i in recv_list:
            try:
                msg = messenger.recv(i)
                print "<got '{}'>".format(msg)
                self.inbox.append(msg)
            except messenger.ClosedConnection:
                i.close()
        for i in error_list:
            print "<socket exception...>"
            i.close()

    def has_messages(self):
        return len(self.inbox) > 0

    def get_message(self):
        return self.inbox.popleft()

    # tell server to notify all clients that a game's level list has changed
    def send_gameupdate(self, level_list, game_id, user_idx):
        print "netmgrlow: sending gameupdate to server"
        self._send(("gameupdate", [game_id, user_idx, level_list]))

    def recv_gameupdate(self, level_list, game_id):
        print "netmgrlow: receiving gameupdate from server"
        
    def register(self, username, server):
        """Register to a server by username.
        Exceptions: ServerNotFound, InvalidFormat, UsernameUnavailable
        """
        if len(username) < 3:
            raise InvalidFormat
        self._join_server(server)
        self._login(username)

    def unregister(self):
        """Gracefully unregister from server.
        """
        self.conn.close()

    def create_game(self, game_name):
        """Create a game on the server.
        """
        if len(game_name) == 0:
            return
        self._send(("create", game_name))

    def chat(self, msg):
        """Create a game on the server.
        """
        self._send(("chat", msg))

    def join_game(self, game_id):
        """Join a game using the game id (provided in the tuple).
        """
        self._send(("join", game_id))

    def exit_game(self):
        """Exit the game that the user is currently in.
        """
        self._send(("exit",None))

    # -- private --

    def _send(self, msg):
        self.outbox.append(msg)

    def _join_server(self, server):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((server, gameserver.PORT))
            self.conn.setblocking(0)
        except (socket.gaierror, socket.error):
            self.conn = None
            raise ServerNotFound

    def _login(self, username):
        self._send(("login", username))
        while not self.has_messages():
            self.update()
        header, payload = self.get_message()
        if header != "login_result" or payload == False:
            self.conn.close()
            raise UsernameUnavailable


