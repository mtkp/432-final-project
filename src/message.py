# some code taken from https://docs.python.org/2/howto/sockets.html#socket-howto

import cPickle as pickle


# maximum message length
header_size = 4
max_msg_len = (10 ** header_size) - 1
packet      = "{{0:0{}d}}{{1}}".format(header_size)


class MessageTooLarge(Exception):
    """This exception is raised if the message exceeds the maximum allowed
    by the header size.
    """
    def __init__(self, size):
        self.size = size
    def __str__(self):
        return repr("{} exceeds limit of {}".format(self.size, max_msg_len))


class ClosedConnection(Exception):
    """This exception is thrown if trying to read from a socket when the
    connection has been closed.
    """
    pass

# send a message over the connection
def send(conn, data):
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


# receive a message from the connection
def recv(conn):
    length = int(_recv_str(conn, header_size))
    msg = _recv_str(conn, length)
    return pickle.loads(msg)


# receive a string of specified length
def _recv_str(conn, length):
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
