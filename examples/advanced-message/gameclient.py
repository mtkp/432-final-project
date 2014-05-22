#!/usr/bin/python2.7
# gameclient.py

# python libs
import socket

# our libs
import gameserver
import message

class GameClient(object):
    def __enter__(self):
        self.register()

    def __exit__(self, type, value, traceback):
        self.unregister()

    def register(self):
        self._join_server()
        self._login()

    def unregister(self):
        message.send(self.conn, "exit")
        self.conn.close()

    def send(self, content):
        message.send(self.conn, content)

    def recv(self):
        return message.recv(self.conn)

    def _join_server(self):
        # connect to server
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                server = raw_input("server: ")
                self.conn.connect((server, gameserver.PORT))
                break
            except socket.gaierror:
                print "could not connect to server {}".format(server)
            except socket.error:
                print "could not connect to port {}".format(gameserver.PORT)
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _login(self):
        # login with username
        while True:
            self.send(raw_input("username: "))
            if self.recv() == 'success':
                return
            print "error - username unavailable"
