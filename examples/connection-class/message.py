# some code taken from https://docs.python.org/2/howto/sockets.html#socket-howto


MSG_HDR = 4
MSG_FORMAT = "{{0:0{}d}}".format(MSG_HDR)


# send a message over the connection
def send_msg(conn, msg):
    msg = MSG_FORMAT.format(len(msg)) + msg
    totalsent = 0

    while totalsent < len(msg):
        sent = conn.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


# receive a message from the connection
def recv_msg(conn):
    length = int(_recv_str(conn, 4))
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
