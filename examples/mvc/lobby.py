
import base
import events
import util

class LobbyView(base.View):
    GREETING = "Hello, {}!"

    def __init__(self, handler, window):
        base.View.__init__(self, handler, window)
        self.hello = util.Label(
            self.background,
            (200, 30),
            self.font,
            LobbyView.GREETING
            )
        self.users = util.Label(
            self.background,
            (400, 200),
            self.font,
            ""
            )
        self.games = util.Label(
            self.background,
            (400, 400),
            self.font,
            ""
            )
        self.draw_set.extend([
            self.hello,
            self.users,
            self.games
            ])

    def notify(self, event):
        if isinstance(event, events.UserUpdate):
            self.update(event.user)
        if isinstance(event, events.MouseClick):
            self.handler.post_event(events.GetUsers())
        elif isinstance(event, events.KeyPress):
            if chr(event.key) == 'q':
                self.handler.post_event(events.Logout())

    def update(self, user):
        self.hello.text = LobbyView.GREETING.format(user.name)
        self.users.text = ", ".join(user.users)
        self.games.text = ", ".join(
            "{} - {}".format(game[0], ",".join(game[2])) for game in user.games
            )

