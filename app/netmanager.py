#!/usr/bin/python2.7

# File:         netmanager.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:
# Netmanager provides functionality that can be used to communicate over the
# underlying network. It recieves events from the event manager on the client 
# side, and makes use of the netio class to send information corresponding to 
# those events to the server. When the netmanager recieves a message from
# the server, it posts a corresponding event to the local event manager which 
# relays those messages to the rest of the program.  The netmanager checks for 
# messages upon each tick of the clock.


# netmanager.py

# netmanager provides an interface between the network IO and the program
# - network events on each tick, "network_notify"
# - program events through "notify"

import base
import events
import netio


class InvalidFormat(Exception):
    """The given username formatting is invalid."""
    pass

class UsernameUnavailable(Exception):
    """The server rejected the username."""
    pass


class NetManager(base.Listener):
    def __init__(self, handler, model):
        base.Listener.__init__(self, handler)
        self.model = model
        self.handler.register_for_ticks(self)
        self.net_conn = netio.NetIO()

    # handle messages from server by posting events to local event handler
    def network_notify(self, event):
        header, payload = event
        if header == "users":
            self.model.all_users = payload
            self.handler.post_event(events.ModelUpdated())
        elif header == "games":
            self.model.all_games = payload
            self.handler.post_event(events.ModelUpdated())
        elif header == "chat":
            self.model.chat_log.append(payload)
            self.model.chat_log = self.model.chat_log[-6:] # only save last 6 msgs
            self.handler.post_event(events.ModelUpdated())
        elif header == "joined":
            self.model.current_game = payload
            self.handler.post_event(events.UserJoinedGame())
        elif header == "wait_update":
            self.model.current_game = payload
            self.handler.post_event(events.ModelUpdated())
        elif header == "game_update_in":
            self.handler.post_event(events.GameUpdateIn(payload))
        elif header == "start_game":
            self.handler.post_event(events.StartGame())
        elif header == "game_initialize":
            self.handler.post_event(events.GameInitialize(
                payload[0],
                payload[1]
                ))
        elif header == "player_won":
            self.handler.post_event(events.PlayerWon(payload))

    # handle locally generated program events by sending messages to server
    def notify(self, event):
        if isinstance(event, events.TryLogin):
            self.register(event.name, event.server)
        if isinstance(event, events.TryCreateGame):
            self.create_game(event.name)
        if isinstance(event, events.TryJoinGame):
            self.join_game(event.game_id)
        if isinstance(event, events.TrySendChat):
            self.chat(event.msg)
        elif isinstance(event, events.Logout):
            self.unregister()
        elif isinstance(event, events.LeaveGame):
            self.exit_game()
        elif isinstance(event, events.GameStarted):
            self.get_initialized()
        elif isinstance(event, events.GameUpdateOut):
            self.send_game_update(event.user_name)

    # on each tick check for network events
    def tick(self):
        if self.net_conn.conn:
            self.net_conn.update() # update the connection if we have one
        if self.net_conn.has_messages():
            # hand off any network events to be processed
            network_event = self.net_conn.recv()
            self.network_notify(network_event)

    def register(self, name, server):
        try:
            self.net_conn.connect(server)
            self.login(name)
            self.model.username = name
            self.handler.post_event(events.UserLoggedIn())
        except InvalidFormat:
            self.handler.post_event(events.LoginError("Bad format"))
        except UsernameUnavailable:
            self.handler.post_event(events.LoginError("Username is taken"))
        except netio.ServerNotFound:
            self.handler.post_event(events.LoginError("Server not found"))

    def unregister(self):
        self.net_conn.close()
        self.handler.post_event(events.UserLoggedOut())

    # clients tell server about update
    def send_game_update(self, username):
        """Sent a correct word notification to the server.
        """
        self.net_conn.send( ( "game_update_out", username) )

    def create_game(self, game_name):
        """Create a game on the server.
        """
        if len(game_name) == 0:
            return
        self.net_conn.send(("create", game_name))

    def chat(self, msg):
        """Create a game on the server.
        """
        self.net_conn.send(("chat", msg))

    def join_game(self, game_id):
        """Join a game using the game id (provided in the tuple).
        """
        self.net_conn.send(("join", game_id))

    def get_initialized(self):
        self.net_conn.send(("game_initialize", None))

    def exit_game(self):
        """Exit the game that the user is currently in.
        """
        self.net_conn.send(("exit_game", None))

    def login(self, username):
        """Login to a server with given username.
        Exceptions: InvalidFormat, UsernameUnavailable
        """
        if len(username) < 3:
            self.net_conn.update()
            raise InvalidFormat
        self.net_conn.send(("login", username))
        while not self.net_conn.has_messages():
            self.net_conn.update()
        header, payload = self.net_conn.recv()
        if header != "login_result" or payload == False:
            self.net_conn.close()
            raise UsernameUnavailable
