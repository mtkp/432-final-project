#!/usr/bin/python2.7
# server

# python libs
import socket

# our libs
import message


HOST = ''
PORT = 7307
LISTEN_QUEUE = 5


def get_info(conn):
    print "<new connection: {}:{}>".format(*addr)


# set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(LISTEN_QUEUE)

# connect to the client
conn, addr = server.accept()
get_info(conn)

name = message.recv_msg(conn)
print "user {} connected".format(name)

command = ''
while command != "exit":
    command = message.recv_msg(conn)
    print "{}: {}".format(name, command)

conn.close()
