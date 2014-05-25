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

    def send(self, msg):
        message.send(self.conn, msg)

    def recv(self):
        return message.recv(self.conn)

    def run(self):
        # connect to user
        name = self.recv()
        response = ''
        with users_lock:
            if name in users or name in reserved_names:
                response = 'error'
            else:
                response = 'success'
                users.append(name)
        self.send(response)

        if response == 'success':
            self._talk_to_user(name)

            # remove user on signout
            with users_lock:
                users.remove(name)
            print "<user {} disconnected>".format(name)

        print "<thread is terminating connection>"
        conn.close()

    def _talk_to_user(self, name):
        while True:
            response = {
                'exit': 'exit',
                'users': get_users(),
                'games': get_games()
            }.get(self.recv(), "unknown command")

            if response == 'exit':
                return
            else:
                self.send(response)


def get_users():
    copy = None
    with users_lock:
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
    users = []

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


