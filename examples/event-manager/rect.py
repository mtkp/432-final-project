import pygame

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
