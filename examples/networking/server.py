#!/usr/bin/python2.7
# the game server

import socket

HOST = ''
PORT = 7307
LISTEN_QUEUE = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(LISTEN_QUEUE)

conn, addr = server.accept()
print "connected with", addr

conn.close()


