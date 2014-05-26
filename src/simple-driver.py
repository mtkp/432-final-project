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
    print "Game created: '{}' [{}] ({}/{})".format(game[0], game[1], len(game[2]), game[3])
    print "####"

# get server name from user
with gameclient.GameClient() as client:

    current_game = None

    while True:
        username = raw_input("username: ")
        server = "localhost" # raw_input("server: ")

        try:
            client.register(username, server)
            break
        except gameclient.InvalidFormat:
            print "format was bad"
        except gameclient.UsernameUnavailable:
            print "user name is taken"
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
                print_game(result)
                current_game = result[1]
        elif command == 'join game':
            result = client.join_game(int(raw_input("game id: ")))
            if result:
                current_game = result[1]
                print "success! joined {}".format(result[0])
            else:
                print "unable to join game"
        elif command == 'exit game':
            result = client.exit_game(current_game)
            if result:
                print "exited game"

