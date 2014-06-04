# File:         messenger.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse

# Assignment:   Final Project

# Description:


# python modules
import cPickle as pickle


header_size = 4
max_msg_len = (10 ** header_size) - 1
packet      = "{{0:0{}d}}{{1}}".format(header_size)


class MessageTooLarge(Exception):
    '''This exception is raised if the message exceeds the maximum allowed
    by the header size.
    '''
    def __init__(self, size):
        self.size = size
    def __str__(self):
        return repr("{} exceeds limit of {}".format(self.size, max_msg_len))


class ClosedConnection(Exception):
    '''This exception is thrown if trying to read from a socket when the
    connection has been closed.
    '''
    pass


def send(conn, data):
    '''Send a message over the given connection.
    '''
    msg = pickle.dumps(data)
    msg_len = len(msg)
    if msg_len > max_msg_len:
        raise MessageTooLarge(msg_len)

    # prepend message with header
    msg = packet.format(msg_len, msg)
    totalsent = 0
    while totalsent < len(msg):
        sent = conn.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def recv(conn):
    '''Receive a message on the given connection.
    '''
    length = int(_recv_str(conn, header_size))
    msg = _recv_str(conn, length)
    return pickle.loads(msg)

def _recv_str(conn, length):
    '''Receive a specific number of bytes on a connection.
    '''
    msg = conn.recv(length)
    if msg:
        while len(msg) < length:
            chunk = conn.recv(length - len(msg))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            msg = msg + chunk
        return msg
    else:
        raise ClosedConnection
