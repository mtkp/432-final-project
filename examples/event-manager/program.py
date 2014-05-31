#!/usr/bin/python2.7

import pygame

import color
import game
import gameclient
import rect


FRAMERATE = 30

userinput = None

class UserInput(object):
    def update(self):
        self.events = pygame.event.get()


class BorderBox(object):
    def __init__(self, background, center, size, fill_color):
        border_size = size[0] + 2, size[1] + 2
        self.border = rect.Rectangle(background, center, border_size, color.Black)
        self.box = rect.Rectangle(background, center, size, fill_color)

    def draw(self):
        self.border.draw()
        self.box.draw()

    def set_color(self, color):
        self.box.set_color(color)

    def collidepoint(self, xy):
        return self.box.collidepoint(xy)

class Text(object):
    def __init__(self, text, background, center):
        self.background = background
        self.font = pygame.font.SysFont("monospace", 20)
        self.surface = self.font.render(text, 1, color.Black)
        self.rect = self.surface.get_rect()
        self.rect.center = center

    def draw(self):
        self.background.blit(self.surface, self.rect)

class TextBox(object):
    def __init__(self, text, background, center, size):
        self.background = background
        self.text = Text(text, background, center)
        self.box  = BorderBox(background, center, size, color.White)

    def draw(self):
        self.box.draw()
        self.text.draw()

    def update(self):
        pass

    def set_color(self, color):
        self.box.set_color(color)

class InputBox(object):
    def __init__(self, text, background, center, size):
        self.background = background
        self.center = center
        self.size = size
        self.text = [c for c in text]
        self.box = BorderBox(background, center, size, color.LightGray)
        self.focus = rect.Rectangle(background, center, size, color.White)
        self._draw_text_box()
        self.active = False

    def _draw_text_box(self):
        self.text_box = Text(
            "".join(self.text),
            self.background,
            self.center,
        )
        self.text_box.rect.left = self.box.box.rect.left + 4
        self.text_box.draw()

    def draw(self):
        self.box.draw()
        if self.active:
            self.focus.draw()
        self._draw_text_box()

    def update(self):
        for event in userinput.events:
            if event.type == event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.box.collidepoint(mouse):
                    self.active = True
                else:
                    self.active = False
            if self.active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[0:-1]
                elif event.key <= 127:
                    self.text.append(chr(event.key))

class Button(object):
    def __init__(self, text, background, center, size):
        self.box = TextBox(text, background, center, size)
        self.box.set_color(color.White)
        self.active = False

    def draw(self):
        self.box.draw()

    def update(self):
        for event in userinput.events:
            if event.type == event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.box.box.collidepoint(mouse):
                    self.active = True
                    self.box.set_color(color.LightGray)
            elif self.active and pygame.MOUSEBUTTONUP:
                self.box.set_color(color.White)
                self.active = False

class Login(object):
    def __init__(self, background, user):
        self.user = user
        self.background = rect.Rectangle(
            background,
            (400, 300),
            (800, 600),
            color.Gray
        )
        self.name_label = Text("name ", background, (450, 150))
        self.name_input = InputBox("", background, (450, 150), (300, 28))
        self.name_label.rect.right = self.name_input.box.box.rect.left

        self.server_label = Text("server ", background, (450, 250))
        self.server_input = InputBox("", background, (450, 250), (300, 28))
        self.server_label.rect.right = self.server_input.box.box.rect.left

        self.login_button = Button("login", background, (550, 350), (100, 30))



    def update(self):
        self.name_input.update()
        self.server_input.update()
        self.login_button.update()

    def draw(self):
        self.background.draw()
        self.name_label.draw()
        self.name_input.draw()
        self.server_label.draw()
        self.server_input.draw()
        self.login_button.draw()

class Program(object):
    def run(self):
        global userinput

        # initialize game
        pygame.init()
        userinput = UserInput()
        clock     = pygame.time.Clock()
        screen    = pygame.display.set_mode((800, 600))
        screen.fill(color.Black)
        pygame.display.set_caption('CSS 432 Game')

        # initialize game objects
        user         = gameclient.GameClient()
        login_screen = Login(screen, user)
        # lobby_screen = Lobby(screen, user)
        game_screen  = game.Game(screen, user)

        focus = login_screen
        while True:
            clock.tick(FRAMERATE)
            userinput.update()

            for event in userinput.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            focus.update()
            focus.draw()

            pygame.display.flip()





if __name__ == '__main__':
    program = Program()
    program.run()