#!/usr/bin/python2.7
# gameclient.py

# python libs
import socket

# our libs
import gameserver
import message


class InvalidFormat(Exception):
    """This exception is raised if the given username format is invalid.
    """
    pass

class UsernameUnavailable(Exception):
    """This exception is raised if the given server rejects the username.
    """
    pass

class ServerNotFound(Exception):
    """This exception is raised if unable to connect to the given server.
    """
    pass

class GameClient(object):
    def register(self, username, server):
        """Register to a server by username.
        Exceptions: ServerNotFound, InvalidFormat, UsernameUnavailable
        """
        self._join_server(server)
        self._login(username)

    def unregister(self):
        try:
            self._send("exit")
        except:
            pass
        try:
            self.conn.close()
        except:
            pass

    def get_users(self):
        self._send("users")
        return self._recv()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.unregister()

    def _send(self, msg):
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
        if len(username) == 0:
            raise InvalidFormat
        self._send(username)
        if self._recv() == 'error':
            self.conn.close()
            raise UsernameUnavailable
