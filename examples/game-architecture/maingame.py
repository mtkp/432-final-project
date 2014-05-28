#!/usr/bin/python2.7

import pygame

FRAMERATE = 30

Black =   0,   0,   0
Red   = 150,   0,   0
Green =   0, 150,   0
Blue  =   0,   0, 150
DarkBlue  =  10,  10, 100
White = 255, 255, 255


QUIT    = pygame.QUIT
CLICK   = pygame.MOUSEBUTTONDOWN
RELEASE = pygame.MOUSEBUTTONUP

game_input = None


class GameInput(object):
    def update(self):
        self.events = pygame.event.get()


class Timer(object):
    def __init__(self, initial_time):
        self.initial_time = initial_time
        self.reset()

    def reset(self):
        self.ticks = FRAMERATE * self.initial_time

    def update(self):
        self.ticks -= 1

    def is_done(self):
        return self.ticks < 1


class Rectangle(object):
    def __init__(self, background, center, size, color):
        self.background = background
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.center = center
        self.set_color(color)

    def draw(self):
        self.background.blit(self.surface, self.rect)

    def set_color(self, color):
        self.color = color
        self.surface.fill(self.color)

    def collidepoint(self, xy):
        return self.rect.collidepoint(xy)


class ColorChanger(object):
    def __init__(self, background, center, size, start_color, end_color):
        self.start_color = start_color
        self.end_color = end_color

        self.box = Rectangle(background, center, size, self.start_color)
        self.timer = Timer(5)

    def update(self):
        self.timer.update()
        if self.timer.is_done():
            if self.box.color == self.start_color:
                self.box.set_color(self.end_color)
            else:
                self.box.set_color(self.start_color)
            self.timer.reset()

    def draw(self):
        self.box.draw()


class Clicker(object):
    def __init__(self, screen, center, size, color):
        self.color = color
        self.box = Rectangle(screen, center, size, self.color)

    def update(self):
        for event in game_input.events:
            if event.type == CLICK:
                mouse = pygame.mouse.get_pos()
                if self.box.collidepoint(mouse):
                    self.box.set_color(DarkBlue)
            elif event.type == RELEASE and self.box.color == DarkBlue:
                self.box.set_color(self.color)

    def draw(self):
        self.box.draw()


class Game(object):
    def run(self):
        global game_input

        pygame.init()
        game_input = GameInput()

        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((640, 480))
        screen.fill(Black)
        pygame.display.set_caption('432 game')

        c = ColorChanger(screen, (300, 300), (70, 70), Red, Blue)
        d = ColorChanger(screen, (300, 400), (70, 70), Green, Red)
        e = ColorChanger(screen, (320, 350), (80, 80), Blue, Green)

        f = Clicker(screen, (100, 100), (50, 50), Blue)

        while True:
            clock.tick(FRAMERATE)
            game_input.update()
            for event in game_input.events:
                if event.type == QUIT:
                    pygame.quit()
                    return

            c.update()
            d.update()
            e.update()
            f.update()

            c.draw()
            e.draw()
            d.draw()
            f.draw()

            pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.run()

