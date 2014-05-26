#!/usr/bin/python2.7

import selectserver


PORT = 7307


class Game(object):
    def __init__(self, name, size):
        self.players = []
        self.name = name
        self.size = size

    def add_user(self, user):
        user.game = self
        self.players.append(user)

    def remove_user(self, user):
        if user in self.players:
            self.players.remove(user)
            user.game = None
            return True
        return False

    def usernames(self):
        return [user.name for user in self.players]

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
                if id(game) == game_id:
                    game.add_user(user)
                    user.send(game.compact())
                    break
            else:
                user.send(False)
        else:
            user.send(False)

    def in_game(self, user):
        msg = user.recv()
        cmd = msg[0]
        if cmd == "users":
            user.send(user.game.usernames())
        elif cmd == "exit":
            game_id = msg[1]
            for game in self.games:
                if id(game) == game_id:
                    user.send(game.remove_user(user))
                    break
            else:
                user.send(False)
        else:
            user.send(False)

    def serve_forever(self):
        while True:
            self.server.update()
            self.games = filter(lambda g: len(g.players) > 0, self.games)
            self.usernames = [
                user.name for user in self.server.users() if user.name
            ]

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

