#!/usr/bin/python2.7

import gameclient


# an easy way to connect multiple clients to the server
# for testing filling up the user list

clients = []
while True:
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


    while not client.has_messages():
        client.update()

    print "{} -- {}".format(*client.get_message())
    clients.append(client)
