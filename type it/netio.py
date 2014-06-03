#

# File:         .py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:


# netio.py

# handle the actual input and output to and from the network

# python libs
import socket
import select
import collections

# our libs
import gameserver
import messenger


class ServerNotFound(Exception):
    """Unable to connect to the given server."""
    pass


class NetIO(object):
    def __init__(self):
        self.outbox = collections.deque()
        self.inbox  = collections.deque()
        self.conn   = None

    def has_messages(self):
        return len(self.inbox) > 0

    def recv(self):
        return self.inbox.popleft()

    def send(self, msg):
        self.outbox.append(msg)

    def update(self):
        """Get the next message from the TCP buffer if available, and add
        to inbox.
        Send the next message in the outbox if it is not empty.
        """
        recv_list, send_list, error_list = \
            select.select([self.conn], [self.conn], [self.conn], 0)

        # for each of those port we want to send out on, send
        for i in send_list:
            if len(self.outbox) > 0:
                messenger.send(i, self.outbox.popleft())
        # for each port we want to receive on, print data received
        for i in recv_list:
            try:
                msg = messenger.recv(i)
                print "<got '{}'>".format(msg)
                self.inbox.append(msg)
            except messenger.ClosedConnection:
                self.close()

        for i in error_list:
            print "<socket exception...>"
            self.close()

    def connect(self, server):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            self.conn.connect((server, gameserver.PORT))
            # switch to nonblocking after connecting so we can do DNS lookup
            self.conn.setblocking(0)
        except (socket.gaierror, socket.error):
            self.close()
            raise ServerNotFound

    def close(self):
        self.conn.close()
        self.conn = None
