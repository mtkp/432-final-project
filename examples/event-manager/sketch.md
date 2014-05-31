
# sketch


``` py
# high level game interface
class Game(object):
  def __init__( main_window_surface )
    self.hero = Hero()
    self.enemy = Enemy()

  def update(self)
    self.enemy.update()
    self.hero.update()

  def draw(self)
    self.enemy.draw()
    self.hero.draw()


# event object --> userinput
userinput = UserInput() # t.b.d.
# userinput will contain list of current events
# but eventually this will hopefully be a dict for O(1) access
# to use it:
for event in program.userinput:
  # your event code here
  # don't modify the actual event object.. this is needed



# the main program loop
class Program(object):
  def run(self):
    pygame.init()

    start_screen = StartScreen()
    lobby = Lobby()
    game = Game()

    while True:
      userinput.update()

      if lobby_state:
        lobby.update()
        lobby.draw()

      elif login_state:
        start_screen.update()
        start_screen.draw()

      elif game_state:
        game.update()
        game.draw()
```




