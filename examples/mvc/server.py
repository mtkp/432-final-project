#!/usr/bin/python2.7

import gameserver

if __name__ == "__main__":
    server = gameserver.GameServer()
    print "<starting gameserver>"
    server.serve_forever()
