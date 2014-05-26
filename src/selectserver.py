#!/usr/bin/python2.7
# multithreaded game server

# python libs
import collections
import select
import socket

# our libs
import message

LISTEN_QUEUE = 5

class User(object):
    def __init__(self, conn):
        self.conn   = conn
        self.inbox  = collections.deque()
        self.outbox = collections.deque()
        self.name   = None
        self.game   = None

    def has_messages(self):
        return len(self.inbox) > 0

    def recv(self):
        return self.inbox.popleft()

    def send(self, msg):
        self.outbox.append(msg)


class Server(object):
    def __init__(self, port):
        # set up non-blocking server socket with reuse option
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('',port))
        self.server.listen(LISTEN_QUEUE)

        # map socket fds to User objects
        self._users = {}

    def users(self):
        return self._users.itervalues()

    def update(self):
        """Send and receive to and from any server sockets.
        """
        recv_list = [u.conn for u in self.users()]
        recv_list.append(self.server)
        send_list = [u.conn for u in self.users() if len(u.outbox) > 0]

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
            self._users[new_conn] = User(new_conn)
        else:
            try:
                data = message.recv(conn) # what if we want more than 1024?
                print "<got '{}'>".format(data)
                self._users[conn].inbox.append(data)
            except message.ClosedConnection:
                self._close(conn)

    def _send(self, conn):
        response = self._users[conn].outbox.popleft()
        print "<sending '{}'>".format(response)
        message.send(conn, response)

    def _close(self, conn):
        print "<closing connection>"
        user = self._users[conn]
        if user.game:
            user.game.remove_user(user)
        del self._users[conn]
        conn.close()
