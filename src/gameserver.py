#!/usr/bin/python2.7

import selectserver


PORT = 7307


class Game(object):
    def __init__(self, name, size):
        self.users = []
        self.name = name
        self.size = size

    def add_user(self, user):
        user.game = self
        self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
            user.game = None

    def usernames(self):
        return [user.name for user in self.users]

    def compact(self):
        return (self.name, id(self), self.usernames(), self.size)


class GameServer(object):
    def __init__(self, port):
        self.server    = selectserver.Server(port)
        self.games     = []
        self.usernames = []

    def register(self, user):
        cmd, name = user.recv()
        if cmd == "login" and name not in self.usernames:
            user.name  = name
            user.send(True)
        else:
            user.send(False)

    def in_lobby(self, user):
        msg = user.recv()
        cmd = msg[0]
        if cmd == "users":
            user.send(self.usernames)
        elif cmd == "games":
            user.send([game.compact() for game in self.games])
        elif cmd == "create":
            new_game = Game(msg[1], 4)
            new_game.add_user(user)
            self.games.append(new_game)
            user.send(new_game.compact())
        elif cmd == "join":
            game_id = msg[1]
            for game in self.games:
                if id(game) == game_id and len(game.users) < game.size:
                    game.add_user(user)
                    user.send(game.compact())
                    break
            else:
                user.send(False)
        else:
            user.send(False)

    def in_game(self, user):
        game = user.game
        msg = user.recv()
        cmd = msg[0]
        if cmd == "users":
            user.send(game.usernames())
        elif cmd == "exit":
            game.remove_user(user)
            user.send(True)
        else:
            user.send(False)

    def serve_forever(self):
        while True:
            self.server.update()

            # clean up games
            self.games = filter(lambda game: len(game.users) > 0, self.games)

            # get list of usernames
            self.usernames = [
                user.name for user in self.server.users() if user.name
            ]

            # handle requests
            for user in self.server.users():
                while user.has_messages():
                    if user.name is None:
                        self.register(user)
                    elif user.game is None:
                        self.in_lobby(user)
                    else:
                        self.in_game(user)


if __name__ == "__main__":
    server = GameServer(PORT)
    print "<starting server on port {}>".format(PORT)
    server.serve_forever()

