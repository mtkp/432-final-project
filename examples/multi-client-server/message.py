# some code taken from https://docs.python.org/2/howto/sockets.html#socket-howto

# send a message over the connection
def send_msg(conn, msg):
    msg = "{0:04d}".format(len(msg)) + msg
    totalsent = 0

    while totalsent < len(msg):
        sent = conn.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


# receive a message from the connection
def recv_msg(conn):
    length = int(recv_str(conn, 4))
    return recv_str(conn, length)


# receive a string of specified length
def recv_str(conn, length):
    msg = ''

    while len(msg) < length:
        chunk = conn.recv(length - len(msg))
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg = msg + chunk

    return msg
