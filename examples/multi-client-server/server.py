#!/usr/bin/python2.7
# multithreaded server

# python libs
import socket
import threading

# our libs
import message


HOST = ''
PORT = 29717
LISTEN_QUEUE = 5


# lock for shared user list
users_lock = threading.Lock()
users = []


# connection threads
# - listen to connected user for commands
# - available commands are
#   hello
#   who/list
#   exit/quit
class ConnThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        print "<starting thread>"

        # connect to user
        name = message.recv_msg(self.conn)
        print "<user {} connected>".format(name)

        # add user to list of users
        with users_lock:
            users.append(name)

        command = ''
        while command != "exit" and command != "quit":
            command = message.recv_msg(self.conn)
            print "<{}: {}>".format(name, command)

            # various commands
            response = ""
            if command == "hello":
                response = " - Hello, world!"
            elif command == "list" or command == "who":
                with users_lock:
                    response = '\n'.join([" - " + u for u in users])
            elif command == "exit" or command == "quit":
                response = " - server is closing connection"
            else:
                response = " - unknown command '{}'".format(command)

            message.send_msg(self.conn, response)

        # remove user on signout
        with users_lock:
            users.remove(name)

        conn.close()


# main thread
# - accepts new connections
# - creates new thread for that connection

# set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(LISTEN_QUEUE)

# connect to the client
while True:
    conn, addr = server.accept()
    print "<new connection>"
    ConnThread(conn).start() # start thread


