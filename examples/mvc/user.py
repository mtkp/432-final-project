
import base
import events
import gameclient


class User(base.Model):
    def __init__(self, handler):
        base.Model.__init__(self, handler)
        self.client = gameclient.GameClient()
        self.name   = None

    def notify(self, event):
        if isinstance(event, events.TryLogin):
            self.register(event.name, event.server)
        elif isinstance(event, events.GetUser):
            self.handler.post_event(events.User(self.name))
        elif isinstance(event, events.GetUsers):
            self.get_users()
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

    def get_users(self):
        users = self.client.get_users()
        if users:
            self.handler.post_event(events.Users(users))

