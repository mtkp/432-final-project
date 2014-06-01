
import base
import events
import netmanagerlow


# wrap the while loop from bottom of client test, check header

class NetManagerHigh(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.handler.register_for_ticks(self)
        self.net_manager_low = netmanagerlow.NetManagerLow()
        self.name   = None
        self.users  = []
        self.games  = []
        
        # current game ( "name", id, ["bob", "joe", "steve"], 4 )
        # ( "game_update", [1, 4, 7, 2] )

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

    def notify(self, event):
        if isinstance(event, events.TryLogin):
            self.register(event.name, event.server)
        elif isinstance(event, events.GetUser):
            self.handler.post_event(events.UserUpdate(self))
        elif isinstance(event, events.Logout):
            self.unregister()
        elif isinstance(event, events.JoinGame):
            pass
        elif isinstance(event, events.GameUpdateOut):
            # player has updated list to give server
            print "netmgrhigh: got gameupdateoutevent"
            self.net_manager_low.send_server_gameupdate(event.level_list, event.game_id)    
        elif isinstance(event, events.GameUpdateIn):
            # since someone changed, need to tell everyone else 
            print "netmgrhigh: got gumeupdateinevent"
            #pass
    
    # give update to network to tell server there was an update
    def send_server_gameupdate(self, user_index):
        self.net_manager_low.send_server_gameupdate(user_index_list, gameid)



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

