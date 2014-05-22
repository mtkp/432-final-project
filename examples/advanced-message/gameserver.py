#!/usr/bin/python2.7
# multithreaded game server

# python libs
import socket
import threading

# our libs
import message

HOST = ''
PORT = 29717
LISTEN_QUEUE = 5
reserved = ["", "server", "exit", "who"]


# connection threads
# - listen to connected user for commands
class ConnThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        # connect to user
        name = ''
        response = ''
        while response != 'success':
            name = message.recv(self.conn)

            # make sure name is unique
            with users_lock:
                if name in users or name in reserved:
                    response = 'error'
                else:
                    response = 'success'
                    users.append(name)
            message.send(self.conn, response)

        while True:
            command = message.recv(self.conn)
            print "<{}: {}>".format(name, command)

            if command == "exit":
                print "<user {} disconnected>".format(name)
                break
            elif command == "hello":
                response = "Hello, world!"
            elif command == "who":
                with users_lock:
                    response = users
            else:
                response = "unknown command '{}'".format(command)

            message.send(self.conn, response)


        # remove user on signout
        with users_lock:
            users.remove(name)

        conn.close()


if __name__ == "__main__":
    # main thread
    # - accepts new connections
    # - creates new thread for that connection

    # lock for shared user list
    users_lock = threading.Lock()
    users = []

    # set up the server
    print "<starting server on port {}>".format(PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen(LISTEN_QUEUE)

    # connect to the client
    while True:
        conn, addr = server.accept()
        print "<new connection>"
        ConnThread(conn).start() # start thread


