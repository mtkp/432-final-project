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

    def network_notify(self, event):
        header, payload = event
        if header == "users":
            self.model.all_users = payload
            self.handler.post_event(events.ModelUpdated())
        elif header == "games":
            self.games = payload
            self.handler.post_event(events.ModelUpdated())
        elif header == "chat":
            self.model.chat_log.append(payload)
            self.model.chat_log = self.model.chat_log[-6:] # only save last 6 msgs
            self.handler.post_event(events.ModelUpdated())
        elif header == "joined":
            self.model.current_game = payload
            self.handler.post_event(events.UserJoinedGame(payload))
        elif header == "game_update_in":
            self.handler.post_event(event.GameUpdateIn(payload[0], payload[1]))
        elif header == "wait_update":
            self.handler.post_event(events.OtherJoinedWait(payload))
        elif header == "user_game_started":
            self.handler.post_event(events.UserGameStarted())
        elif header == "end_game":
            self.handler.post_event(event.EndGame(payload[0]))

    # handle program events
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
        elif isinstance(event, events.GameUpdateOut):
            self.send_gameupdate_to_server(event.level_list)

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
    def send_gameupdate_to_server(self, level_list):
        print "netmgrlow: sending gameupdate to server"
        self.net_conn.send( ( "update_levels", level_list ) )

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

    def exit_game(self):
        """Exit the game that the user is currently in.
        """
        self.net_conn.send(("exit_game", None))

    def login(self, username):
        """Login to a server with given username.
        Exceptions: InvalidFormat, UsernameUnavailable
        """
        if len(username) < 3:
            raise InvalidFormat
        self.net_conn.send(("login", username))
        while not self.net_conn.has_messages():
            self.net_conn.update()
        header, payload = self.net_conn.recv()
        if header != "login_result" or payload == False:
            self.conn.close()
            self.conn = None
            raise UsernameUnavailable
