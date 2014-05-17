#!/usr/bin/python2.7

import socket
#Client    

#create an INET, STREAMing socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

#now connect to the web server on port 7307
s.connect(("uw1-320-15.uwb.edu", 7307))
h
name = "Greg"
len_name = "{0:04d}".format(len(name))

length = len(name)
total_len = length + len(len_name)
msg = len_name + name
totalsent = 0

while totalsent < total_len:
    sent = s.send(msg[totalsent:])
    if sent == 0:
        raise RuntimeError("socket connection broken")
    totalsent = totalsent + sent

s.close()


