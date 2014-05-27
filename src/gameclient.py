#!/usr/bin/python2.7
# gameclient.py

# python libs
import socket

# our libs
import gameserver
import message

class InvalidFormat(Exception):
    """The given username formatting is invalid."""
    pass

class UsernameUnavailable(Exception):
    """The server rejected the username."""
    pass

class ServerNotFound(Exception):
    """Unable to connect to the given server."""
    pass

class GameClient(object):
    def register(self, username, server):
        """Register to a server by username.
        Exceptions: ServerNotFound, InvalidFormat, UsernameUnavailable
        """
        self._join_server(server)
        self._login(username)

    def unregister(self):
        """Gracefully unregister from server."""
        self.conn.close()

    def get_users(self):
        """Get a list of connected users."""
        self._send("users")
        return self._recv()

    def get_games(self):
        """Get a list of game tuples (game name, id, list of users, size)."""
        self._send("games")
        return self._recv()

    def create_game(self, game_name):
        """Create a game on the server."""
        if len(game_name) == 0:
            return False
        self._send("create", game_name)
        return self._recv()

    def join_game(self, game_id):
        """Join a game using the game id (provided in the tuple)."""
        self._send("join", game_id)
        return self._recv()

    def exit_game(self):
        """Exit the game that the user is currently in."""
        self._send("exit")
        return self._recv()

    # TODO ... will likely change a lot
    def update_positions(self, position):
        # send position to other game players
        self._send("bcast", position)
        return self._recv() # server returns tuple of latest positions of others


    # -- private --

    def _send(self, *msg):
        message.send(self.conn, msg)

    def _recv(self):
        return message.recv(self.conn)

    def _join_server(self, server):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((server, gameserver.PORT))
        except (socket.gaierror, socket.error):
            self.conn = None
            raise ServerNotFound

    def _login(self, username):
        if len(username) < 2:
            raise InvalidFormat
        self._send("login", username)
        success = self._recv()
        if not success:
            self.conn.close()
            raise UsernameUnavailable
