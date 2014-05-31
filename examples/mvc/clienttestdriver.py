#!/usr/bin/python2.7

import time

import gameclient

client = gameclient.GameClient()
# make gameobject register send message

#!/usr/bin/python2.7
# client

# our libs
import gameclient


def print_users(user_list):
    print '\n'.join(" - {}".format(user) for user in user_list)

def print_games(game_list):
    print '\n'.join(
        "'{}' [{}] ({}/{})".format(game[0], game[1], len(game[2]), game[3])
        for game in game_list)

def print_game(game):
    print "####"
    print "'{}' [{}] ({}/{})".format(game[0], game[1], len(game[2]), game[3])
    print_users(game[2])
    print "####"

# get server name from user

client = gameclient.GameClient()

while True:
    username = raw_input("username: ")
    server = "10.0.1.14" # raw_input("server: ")

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
    msg = client.get_messages()
    
    
    if msg:
        print str(msg[0])

    time.sleep(0.04)

    client._send(("test", "test"))
   
