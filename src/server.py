#!/usr/bin/python2.7

import gameserver

class Game(object):
    def __init__(self, name, size):
        self.players = []
        self.name = name
        self.size = size

    def add_player(self, client):
        self.players.append(client)

    def remove_player(self, client):
        if client not in self.players:
            return False
        self.players.remove(client)
        return True

    def compact(self):
        players = [player.username for player in self.players]
        return (self.name, id(self), players, self.size)


def register(client, msg, user_list):
    request, username = msg
    if request != 'login' or username in user_list:
        client.send(False)
    else:
        client.username = username
        client.send(True)


if __name__ == "__main__":
    server = gameserver.GameServer()
    games = []

    while True:
        server.update()

        # --- server logic ---
        users = [c.username for c in server.clients() if c.username]
        for client in server.clients():
            if client.has_messages():
                msg = client.recv()
                cmd = msg[0]
                if client.username is None:
                    register(client, msg, users)
                elif cmd == "users":
                    client.send(users)
                elif cmd == "games":
                    client.send([game.compact() for game in games])
                elif cmd == "create":
                    new_game = Game(msg[1], 4)
                    new_game.add_player(client)
                    games.append(new_game)
                    client.send(new_game.compact())
                elif cmd == "join":
                    game_id = msg[1]
                    for game in games:
                        if id(game) == game_id:
                            game.add_player(client)
                            client.send(game.compact())
                            break
                    else:
                        client.send(False)
                elif cmd == "exit":
                    game_id = msg[1]
                    for game in games:
                        if id(game) == game_id:
                            client.send(game.remove_player(client))
                            break
                    else:
                        client.send(False)
                else:
                    client.send("unknown command")



