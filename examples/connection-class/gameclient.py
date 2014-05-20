#!/usr/bin/python2.7
# gameclient.py

# python libs
import socket

# our libs
from message import send_msg, recv_msg


SERVER_PORT = 29717


class GameClient(object):
    def __init__(self, server):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.conn.connect((self.server, SERVER_PORT))

    def __enter__(self):
        # login with username
        name = raw_input("username: ")
        send_msg(self.conn, name)

    def __exit__(self, type, value, traceback):
        send_msg(self.conn, "exit")
        self.conn.close()

    def send(self, content):
        send_msg(self.conn, content)

    def recv(self):
        return recv_msg(self.conn)
