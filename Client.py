#!/usr/bin/python2.7

import socket
#Client

#create an INET, STREAMing socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

#now connect to the web server on port 7307
s.connect(("uw1-320-15.uwb.edu", 7307))

s.close()


