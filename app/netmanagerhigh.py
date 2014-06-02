import base
import events
import netmanagerlow


# wrap the while loop from bottom of client test, check header

# high = networkmgr
class NetManagerHigh(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.handler.register_for_ticks(self)
        self.net_manager_low = netmanagerlow.NetManagerLow()
        self.name = None
        self.users = []
        self.games = []
        self.chat_log = []

        # current game ( "name", id, ["bob", "joe", "steve"], 4 )
        # ( "game_update", [1, 4, 7, 2] )

    # these are mesages that come in from the server
    def tick(self):
        # if user registered (add registered field)
        if self.net_manager_low.conn:
            self.net_manager_low.update()
        if self.net_manager_low.has_messages():
            header, payload = self.net_manager_low.get_message()
            # read header
            # update appropriate filed
            if header == "users":
                self.users = payload
                self.handler.post_event(events.UserUpdate(self))
            elif header == "games":
                self.games = payload
                self.handler.post_event(events.UserUpdate(self))
            elif header == "chat":
                self.chat_log.append(payload)
                self.chat_log = self.chat_log[-6:] # only save the last 6 msgs
                self.handler.post_event(events.UserUpdate(self))
            
            elif header == "joined":
                self.handler.post_event(events.UserJoinedGame(payload))
            elif header == "game_update_in":
                self.handler.post_event(event.GameUpdateIn(payload[0], payload[1]))
                # why pass in self here?
            elif header == "end_game":
                self.handler.post_event(event.EndGame(payload[0]))

    # these are messages going out to the server
    def notify(self, event):
        if isinstance(event, events.TryLogin):
            self.register(event.name, event.server)
        if isinstance(event, events.TryCreateGame):
            self.net_manager_low.create_game(event.name)
        if isinstance(event, events.TryJoinGame):
            self.net_manager_low.join_game(event.game_id)
        if isinstance(event, events.TrySendChat):
            self.net_manager_low.chat(event.msg)
        elif isinstance(event, events.Logout):
            self.unregister()
        elif isinstance(event, events.LeaveGame):
            self.net_manager_low.exit_game()
        elif isinstance(event, events.GameUpdateOut):
            self.net_manager_low.send_gameupdate_to_server(event.level_list)


    def register(self, name, server):
        try:
            self.net_manager_low.register(name, server)
            self.name = name
            self.handler.post_event(events.UserLoggedIn())
        except netmanagerlow.InvalidFormat:
            self.handler.post_event(events.LoginError("Bad format"))
        except netmanagerlow.UsernameUnavailable:
            self.handler.post_event(events.LoginError("Username is taken"))
        except netmanagerlow.ServerNotFound:
            self.handler.post_event(events.LoginError("Server not found"))

    def unregister(self):
        self.net_manager_low.unregister()
        self.handler.post_event(events.UserLoggedOut())
