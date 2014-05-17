#!/usr/bin/python2.7
# client

# python libs
import socket

# our libs
import message


SERVER_PORT = 29717


# get server name from user
server = raw_input("server: ")

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# now connect to the web server on port 7307
conn.connect((server, SERVER_PORT))

# send username to server
name = raw_input("username: ")
message.send_msg(conn, name)

# send commands and receive response
command = ''
while command != "exit" and command != "quit":
    command = raw_input("command: ")
    message.send_msg(conn, command)
    print message.recv_msg(conn)

conn.close()

