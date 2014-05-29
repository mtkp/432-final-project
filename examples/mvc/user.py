
import base
import events
import gameclient


class User(base.Model):
    def __init__(self, handler):
        base.Model.__init__(self, handler)
        self.client = gameclient.GameClient()

    def notify(self, event):
        if isinstance(event, events.TryLogin):
            self.register(event.name, event.server)
        if isinstance(event, events.GetUsers):
            self.get_users()

    def register(self, name, server):
        try:
            self.client.register(name, server)
            self.handler.post_event(events.UserLoggedIn())
        except gameclient.InvalidFormat:
            self.handler.post_event(events.LoginError("Bad format"))
        except gameclient.UsernameUnavailable:
            self.handler.post_event(events.LoginError("Username is taken"))
        except gameclient.ServerNotFound:
            self.handler.post_event(events.LoginError("Server not found"))

    def get_users(self):
        users = self.client.get_users()
        if users:
            self.handler.post_event(events.Users(users))

