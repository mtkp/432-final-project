#!/usr/bin/python2.7
# client

# our libs
from gameclient import GameClient

# get server name from user
server = raw_input("server: ")
client = GameClient(server)

with client:
    # send commands to server
    command = ''
    resp = ''
    while resp != ' - server is closing connection':
        client.send(raw_input("command: "))
        resp = client.recv()
        print resp


