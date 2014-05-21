#!/usr/bin/python2.7
# gameclient.py

# python libs
import socket

# our libs
import message
import gameserver

class GameClient(object):
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        message.send(self.conn, "exit")
        self.conn.close()

    def connect(self):
        # connect to server
        while True:
            try:
                server = raw_input("server: ")
                self.conn.connect((server, gameserver.PORT))
                break
            except socket.gaierror:
                print "could not connect to server..."

        # login with username
        while True:
            name = raw_input("username: ")
            message.send(self.conn, name)
            if message.recv(self.conn) == 'error':
                print "username already taken"
            else:
                break

    def send(self, content):
        message.send(self.conn, content)

    def recv(self):
        return message.recv(self.conn)
