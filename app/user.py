
import base
import events
import gameclient


# wrap the while loop from bottom of client test, check header

class User(base.Listener):
    def __init__(self, handler):
        base.Listener.__init__(self, handler)
        self.handler.register_for_ticks(self)
        self.client = gameclient.GameClient()
        self.name   = None
        self.users  = []
        self.games  = []

    def tick(self):
        # if user registered (add registered field)
        if self.client.conn:
            self.client.update()
        if self.client.has_messages():
            header, payload = self.client.get_message()
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

    def register(self, name, server):
        try:
            self.client.register(name, server)
            self.name = name
            self.handler.post_event(events.UserLoggedIn())
        except gameclient.InvalidFormat:
            self.handler.post_event(events.LoginError("Bad format"))
        except gameclient.UsernameUnavailable:
            self.handler.post_event(events.LoginError("Username is taken"))
        except gameclient.ServerNotFound:
            self.handler.post_event(events.LoginError("Server not found"))

    def unregister(self):
        self.client.unregister()
        self.handler.post_event(events.UserLoggedOut())

