#!/usr/bin/python2.7
#client

import socket
import sys

#cs = ClientSocket()

def send_msg(socket, msg):
    len_name = "{0:04d}".format(len(msg))

    length = len(msg)
    total_len = length + len(len_name)
    msg = len_name + msg
    totalsent = 0

    while totalsent < total_len:
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

#-----------------------------------------------------------------
#create an INET, STREAMing socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

#now connect to the web server on port 7307
s.connect(("uw1-320-15.uwb.edu", 7307))

name = raw_input("username: ")
send_msg(s, name)

list_response = raw_input("list?: ")
send_msg(s, list_response)

s.close()


