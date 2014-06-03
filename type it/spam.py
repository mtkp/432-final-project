#!/usr/bin/python2.7

#

# File:         .py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:


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
