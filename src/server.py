#!/usr/bin/python2.7

import gameserver

if __name__ == "__main__":
    server = gameserver.GameServer()
    while True:
        server.update()

        # --- server logic
        usernames = (c.username for c in server.clients())
        for client in server.clients():
            msg = client.recv()
            if not msg:
                continue
            if msg == "users":
                client.send(list(usernames))
            else:
                # user is trying to register
                if msg in usernames:
                    # name is taken
                    client.send(False)
                else:
                    # register user
                    client.username = msg
                    client.send(True)
