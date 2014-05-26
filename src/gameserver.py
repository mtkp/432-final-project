#!/usr/bin/python2.7
# multithreaded game server

# python libs
import Queue
import select
import socket
import threading

# our libs
import message

HOST           = ''
PORT           = 7307
LISTEN_QUEUE   = 5
reserved_names = ["admin"]


class Client(object):
    def __init__(self, conn):
        self.conn = conn
        self.username = None
        self.inbox = Queue.Queue()
        self.outbox = Queue.Queue()

    def recv(self):
        try:
            msg = self.inbox.get_nowait()
        except Queue.Empty:
            msg = None
        return msg

    def send(self, msg):
        self.outbox.put_nowait(msg)



class GameServer(object):
    def __init__(self):
        print "<starting server on port {}>".format(PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)

        # allow socket reuse incase of bad shutdown
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind and listen
        self.server.bind((HOST,PORT))
        self.server.listen(LISTEN_QUEUE)

        self.clients = {}

    def clients(self):
        return self.clients.itervalues()

    def update(self):
        """Send and receive to and from any server sockets.
        """
        print "<server checking for events>"

        recv_list = [c.conn for c in self.clients()]
        recv_list.append(self.server)

        send_list = [
            c.conn for c in self.clients() if not c.outbox.empty()
        ]

        recv_list, send_list, exception_list = \
            select.select(recv_list, send_list, recv_list)

        for conn in recv_list:
            if conn is self.server:
                print "<new connection>"
                new_conn, addr = self.server.accept()
                new_conn.setblocking(0)
                self.clients[new_conn] = Client(new_conn)
            else:
                try:
                    data = message.recv(conn) # what if we want more than 1024?
                    print "<got {}>".format(data)
                    self.clients[conn].inbox.put_nowait(data)
                except message.ClosedConnection:
                    # no data, remove socket
                    print "<closing socket>"
                    conn.close()
                    del self.clients[conn]
        for conn in send_list:
            response = self.clients[conn].outbox.get_nowait()
            print "<sending {}>".format(response)
            message.send(conn, response)
        for conn in exception_list:
            print "<socket exception...>"
            conn.close()
            del self.clients[conn]


if __name__ == "__main__":
    server = GameServer()
    while True:
        server.update()
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






