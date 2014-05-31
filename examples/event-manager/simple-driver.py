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
    server = "localhost" # raw_input("server: ")

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
    command = raw_input("command: ")

    if command == 'games':
        games = client.get_games()
        if games:
            print_games(games)

    elif command == 'users':
        users = client.get_users()
        if users:
            print_users(users)

    elif command == 'create game':
        result = client.create_game(raw_input("game name: "))
        if result:
            print "Game created!"
            print_game(result)

    elif command == 'join game':
        try:
            game_id = int(raw_input("game id: "))
            result = client.join_game(game_id)
            if result:
                print "Joined game!"
                print_game(result)
            else:
                print "unable to join game"
        except ValueError:
            print "bad id format"

    elif command == 'exit game':
        result = client.exit_game()
        if result:
            print "exited game"

