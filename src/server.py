#!/usr/bin/python2.7

import Queue

import gameserver

def register(client, username, user_list):
    if username in user_list:
        client.send(False)
    else:
        client.username = username
        client.send(True)


if __name__ == "__main__":
    server = gameserver.GameServer()
    games = [
        ("Game 1", 3, 4),
        ("Game 2", 1, 4),
        ("Game 3", 2, 4)
    ]

    while True:
        server.update()

        # --- server logic ---
        users = [c.username for c in server.clients() if c.username]
        for client in server.clients():
            try:
                msg = client.recv()
                if msg == "users":
                    client.send(users)
                elif msg == "games":
                    client.send(games)
                else:
                    register(client, msg, users)
            except Queue.Empty:
                pass