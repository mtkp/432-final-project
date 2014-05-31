#!/usr/bin/python2.7
# gameclient.py

# python libs
import socket
import select
import collections

# our libs
import gameserver
import message

class InvalidFormat(Exception):
    """The given username formatting is invalid."""
    pass

class UsernameUnavailable(Exception):
    """The server rejected the username."""
    pass

class ServerNotFound(Exception):
    """Unable to connect to the given server."""
    pass

class GameClient(object):
    def __init__(self):
        self.outbox = collections.deque()
        

    # tell us if something is in the buffer using select
    # to figure out what message type we are getting
    
    def get_messages(self):
        msg = None
        # if client has messages from select
        recv_list, send_list, error_list = select.select([self.conn], [self.conn], [])

        # for each of those port we want to send out on, send
        for i in send_list:
            if len(self.outbox) > 0:
                message.send(i, self.outbox.popleft())
        
        # for each port we want to receive on, print data received
        for i in recv_list:
            try:
                data = message.recv(i) # what if we want more than 1024?
                print "<got '{}'>".format(data)
                msg = data
            except message.ClosedConnection:
                i.close()               

        return msg
        
    
    def register(self, username, server):
        """Register to a server by username.
        Exceptions: ServerNotFound, InvalidFormat, UsernameUnavailable
        """
        if len(username) < 3:
            raise InvalidFormat
        self._join_server(server)
        self._login(username)

    def unregister(self):
        """Gracefully unregister from server."""
        self.conn.close()


    def create_game(self, game_name):
        """Create a game on the server."""
        if len(game_name) == 0:
            return False
        self._send("create", game_name)
        return self._recv()

    def join_game(self, game_id):
        """Join a game using the game id (provided in the tuple)."""
        self._send("join", game_id)
        return self._recv()

    def exit_game(self):
        """Exit the game that the user is currently in."""
        self._send("exit")
        return self._recv()

    # TODO ... will likely change a lot
    def update_positions(self, position):
        # send position to other game players
        return self._recv() # server returns tuple of latest positions of others


    # -- private --


    def _send(self, *msg):
        self.outbox.append(msg)

    def _recv(self):
        return message.recv(self.conn)

    
    def _join_server(self, server):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.conn.connect((server, gameserver.PORT))
        self.conn.setblocking(0)
        #except (socket.gaierror, socket.error):
        #    self.conn = None
        #   raise ServerNotFound

    
    def _login(self, username):
        self._send("login", username)
        msg = None
        while msg is None:
            msg = self.get_messages()
        if msg[1] == False:
            self.conn.close()
            raise UsernameUnavailable
            



        
