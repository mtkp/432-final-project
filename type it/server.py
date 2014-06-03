#!/usr/bin/python2.7

#

# File:         .py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:


import gameserver

if __name__ == "__main__":
    server = gameserver.GameServer()
    print "<starting gameserver>"
    server.serve_forever()
