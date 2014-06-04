# File:         messenger.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse

# Assignment:   Final Project

# Description:
# Messenger provides a simple interface for sending and receiving
# objects through a socket.
#
# - Send:
# Messenger uses the pickle module (actually, cPickle, for speed), and gets
# a string (byte) representation of that object. Messenger then prepends
# the serialization with the number of bytes.
#
# - Recv:
# When recv is called, messenger uses the predetermined header size
# (4 bytes) to know it should read at least this many bytes from the socket.
# The bytes contain the size of the rest of the message, so then messenger
# reads this many bytes from the socket. The remaining bytes of the message
# are then deserialized with pickle, and the resulting object is
# returned to the caller.
#
# To support "select", Messenger throws the ClosedConnection exception if it
# reads from a socket and gets 0 bytes, which is what select uses to indicate
# that a ready read socket is actually being closed by the other end.


# python modules
import cPickle as pickle


header_size = 4
max_msg_len = (10 ** header_size) - 1
packet      = "{{0:0{}d}}{{1}}".format(header_size)


class MessageTooLarge(Exception):
    '''This exception is raised if the message exceeds the maximum allowed
    by the header size. It is used as an error checking exception to indicate
    otherwise unnoticed message truncation.

    Header size is variable so this exception is only thrown if the message
    size exceeds max_msg_len (for 4, this is 9999 bytes).
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
