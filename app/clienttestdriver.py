#!/usr/bin/python2.7

import time

import gameclient

client = gameclient.GameClient()


# get server name from user

client = gameclient.GameClient()

while True:
    username = raw_input("username: ")
    server = raw_input("server: ")

    try:
        client.register(username, server)
        break
    except gameclient.InvalidFormat:
        print "format is bad"
    except gameclient.UsernameUnavailable:
        print "username is taken"
    except gameclient.ServerNotFound:
        print "server was not found"


while True:
    client.update()

    if client.has_messages():
        print "{} -- {}".format(*client.get_message())

    time.sleep(0.1)

    # client._send(("test", "test"))

