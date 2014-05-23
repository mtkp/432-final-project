#!/usr/bin/python2.7
# client

# our libs
import gameclient

# get server name from user
client = gameclient.GameClient()

while True:
    username = raw_input("username: ")
    server = raw_input("server: ")

    try:
        client.register(username, server)
        break
    except gameclient.InvalidFormat:
        print "format was bad"
    except gameclient.UsernameUnavailable:
        print "user name is taken"
    except gameclient.ServerNotFound:
        print "server was not found"


print "Game list"
print "---------"
for game in client.game_list:
    print "{}: {}/{}".format(*game)

while True:
    command = raw_input("command: ")
    if command == "exit":
        print "closing connection..."
        client.unregister()
        break

    client.send(command)
    response = client.recv()
    if type(response) is list:
        print '\n'.join(" - " + str(i) for i in response)
    else:
        print response

print "done."