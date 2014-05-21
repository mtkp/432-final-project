#!/usr/bin/python2.7
# client

# our libs
from gameclient import GameClient

# get server name from user
client = GameClient()
client.connect()

with client:
    # send commands to server
    while True:
        command = raw_input("command: ")
        if command == "quit":
            break
        client.send(command)
        print client.recv()

