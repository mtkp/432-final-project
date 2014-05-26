#!/usr/bin/python2.7
# multithreaded game server

# python libs
import socket
import threading

# our libs
import message

HOST           = ''
PORT           = 29717
LISTEN_QUEUE   = 5
reserved_names = ["admin"]


# connection threads
# - listen to connected user for commands
class ConnThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def _send(self, msg):
        message.send(self.conn, msg)

    def _recv(self):
        return message.recv(self.conn)

    def run(self):
        global users, users_lock
        # connect to user
        name = self._recv()
        login = False
        with users_lock:
            if name not in users and name not in reserved_names:
                login = True
                users.append(name)
        self._send(login)

        if login:
            while True:
                request = self._recv()
                if request == "exit":
                    break
                elif request == "users":
                    print "<{} is getting new list>".format(name)
                    self._send(get_users())
                else:
                    self._send("unknown cmd")

            # remove user on signout
            print "<user {} disconnected>".format(name)
            with users_lock:
                users.remove(name)

        print "<thread is terminating connection>"
        conn.close()


def get_users():
    global users, users_lock
    copy = None
    with users_lock:
        print "<copying user list, len is {}>".format(len(users))
        copy = list(users)
    return copy


def get_games():
    copy = None
    with games_lock:
        copy = list(games)
    return copy


if __name__ == "__main__":
    # main thread
    # - accepts new connections
    # - creates new thread for that connection

    # lock for shared users list
    users_lock = threading.Lock()
    users = ["admin"]

    # lock for shared games list
    games_lock = threading.Lock()
    games = [
        ("game 1", 3, 5),
        ("game 2", 1, 4),
        ("game 3", 3, 7)
    ]

    # set up the server
    print "<starting server on port {}>".format(PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # allow socket reuse incase of bad shutdown
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind and listen
    server.bind((HOST,PORT))
    server.listen(LISTEN_QUEUE)

    # connect to the client
    while True:
        conn, addr = server.accept()
        print "<new connection>"
        ConnThread(conn).start() # start thread


