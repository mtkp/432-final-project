#!/usr/bin/python2.7
# multithreaded game server

# python libs
import collections
import select
import socket

# our libs
import message

HOST         = ''
PORT         = 7307
LISTEN_QUEUE = 5


class Client(object):
    def __init__(self, conn):
        self.conn     = conn
        self.username = None
        self.inbox    = collections.deque()
        self.outbox   = collections.deque()

    def has_messages(self):
        return len(self.inbox) > 0

    def recv(self):
        return self.inbox.popleft()

    def send(self, msg):
        self.outbox.append(msg)


class GameServer(object):
    def __init__(self):
        self._clients = {}
        print "<starting server on port {}>".format(PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # non-blocking server
        self.server.setblocking(0)

        # allow socket reuse incase of bad shutdown
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind and listen
        self.server.bind((HOST,PORT))
        self.server.listen(LISTEN_QUEUE)

    def clients(self):
        return self._clients.itervalues()

    def update(self):
        """Send and receive to and from any server sockets.
        """
        recv_list = [c.conn for c in self.clients()]
        recv_list.append(self.server)
        send_list = [
            c.conn for c in self.clients()
            if len(c.outbox) > 0
        ]

        recv_list, send_list, exception_list = \
            select.select(recv_list, send_list, recv_list)

        for conn in recv_list:
            self._recv(conn)

        for conn in send_list:
            self._send(conn)

        for conn in exception_list:
            print "<socket exception...>"
            self._close(conn)

    def _recv(self, conn):
        if conn is self.server:
            new_conn, addr = self.server.accept()
            new_conn.setblocking(0)
            self._clients[new_conn] = Client(new_conn)
        else:
            try:
                data = message.recv(conn) # what if we want more than 1024?
                print "<got '{}'>".format(data)
                self._clients[conn].inbox.append(data)
            except message.ClosedConnection:
                self._close(conn)

    def _send(self, conn):
        response = self._clients[conn].outbox.popleft()
        print "<sending '{}'>".format(response)
        message.send(conn, response)

    def _close(self, conn):
        print "<closing connection>"
        conn.close()
        del self._clients[conn]
