#!/usr/bin/python2.7

# File:         server.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:
# Launches the gamesrver program which is the server that the program uses.

# our modules
import gameserver

if __name__ == "__main__":
    server = gameserver.GameServer()
    print "<starting gameserver>"
    server.serve_forever()
