#!/usr/bin/python2.7
# the game server

# python libs
import socket

# our libs
import message

HOST = ''
PORT = 7307
LISTEN_QUEUE = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(LISTEN_QUEUE)

client, addr = server.accept()
print "-- connected with {} --".format(addr[0])
print "-- client's port is {} --".format(addr[1])

msg = message.recv_message(client)

print "client says '{}'".format(msg)

msg = message.recv_message(client)

if msg == "list":
    print "client wants list of users"
else:
    print "unknown command"


client.close()
