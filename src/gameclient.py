#!/usr/bin/python2.7
# gameclient.py

# python libs
import socket

# our libs
import gameserver
import message


class InvalidFormat(Exception):
    pass

class UsernameUnavailable(Exception):
    pass

class ServerNotFound(Exception):
    pass

class GameClient(object):
    def register(self, username, server):
        self._join_server(server)
        self._login(username)
        self.game_list = self.recv()

    def unregister(self):
        message.send(self.conn, "exit")
        self.conn.close()

    def send(self, msg):
        message.send(self.conn, msg)

    def recv(self):
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
        self.send(username)
        if self.recv() == 'error':
            self.conn.close()
            raise UsernameUnavailable
