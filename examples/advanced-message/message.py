# some code taken from https://docs.python.org/2/howto/sockets.html#socket-howto

SIZE_FIELD = 4
MSG_FORMAT = "{{0:0{}d}}".format(SIZE_FIELD)
MAX_LEN = (10 ** SIZE_FIELD) - 1

class MessageToLarge(Exception):
    def __init__(self, size):
        self.size = size
    def __str__(self):
        return repr("{} exceeds limit of {}".format(self.size, MAX_LEN))

# send a message over the connection
def send(conn, msg):
    msg_len = len(msg)
    if msg_len > MAX_LEN:
        raise MessageToLarge(msg_len)

    msg = MSG_FORMAT.format(msg_len) + msg
    totalsent = 0
    while totalsent < len(msg):
        sent = conn.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


# receive a message from the connection
def recv(conn):
    length = int(_recv_str(conn, SIZE_FIELD))
    return _recv_str(conn, length)


# receive a string of specified length
def _recv_str(conn, length):
    msg = ''

    while len(msg) < length:
        chunk = conn.recv(length - len(msg))
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg = msg + chunk

    return msg
