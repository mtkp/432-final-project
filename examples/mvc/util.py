
import pygame

from color import Black, White, LightGray

class Box(object):
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

    def colliderect(self, xy):
        return self.rect.colliderect(xy)

    @property
    def center(self):
        return self.rect.center

    @center.setter
    def center(self, center):
        self.rect.center = center

    @property
    def centerx(self):
        return self.rect.centerx

    @centerx.setter
    def centerx(self, centerx):
        self.rect.centerx = centerx

    @property
    def centery(self):
        return self.rect.centery

    @centery.setter
    def centery(self, centery):
        self.rect.centery = centery

    @property
    def left(self):
        return self.rect.left

    @left.setter
    def left(self, left):
        self.rect.left = left

    @property
    def right(self):
        return self.rect.right

    @right.setter
    def right(self, right):
        self.rect.right = right

    @property
    def top(self):
        return self.rect.top

    @top.setter
    def top(self, top):
        self.rect.top = top

    @property
    def bottom(self):
        return self.rect.bottom

    @bottom.setter
    def bottom(self, bottom):
        self.rect.bottom = bottom

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, width):
        self.rect.width = width

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, height):
        self.rect.height = height

    @property
    def size(self):
        return self.rect.size

    @size.setter
    def size(self, size):
        self.rect.size = size


class BorderBox(Box):
    def __init__(self, background, center, size, color, border_color):
        Box.__init__(self, background, center, size, color)
        h, w = size
        size = h + 2, w + 2
        self.border = Box(background, center, size, border_color)

    def draw(self):
        self.border.draw()
        Box.draw(self)

    def set_color(self, color):
        Box.set_color(self, color)


class Label(object):
    def __init__(self, background, center, font, text, color=Black):
        self.background = background
        self.font = font
        self.text = text
        self.center = center
        self.color = color

    def draw(self):
        text_box = self.font.render(self.text, 1, self.color)
        text_rect = text_box.get_rect()
        text_rect.center = self.center
        self.background.blit(text_box, text_rect)


class Button(object):
    def __init__(self, background, center, size, color, font, text):
        self.label = Label(background, center, font, text)
        self.box = BorderBox(background, center, size, color, Black)

    def draw(self):
        self.box.draw()
        self.label.draw()

    def collidepoint(self, xy):
        return self.box.collidepoint(xy)


class InputBox(object):
    def __init__(self, background, center, size, font, limit):
        self.label = Label(background, center, font, "")
        self.box = BorderBox(background, center, size, LightGray, Black)
        self.active = False
        self.limit = limit

    def draw(self):
        if self.active:
            self.box.set_color(White)
        else:
            self.box.set_color(LightGray)

        self.box.draw()
        self.label.draw()

    def collidepoint(self, xy):
        return self.box.collidepoint(xy)

    def input(self, raw):
        if raw == 32 or raw == 45 or raw == 46 or (raw > 47 and raw < 58) or (raw > 96 and raw < 122):
            self.label.text += chr(raw)
            self.label.text = self.label.text[:self.limit]
        elif raw == pygame.K_BACKSPACE:
            self.label.text = self.label.text[0:-1]

    @property
    def text(self):
        return self.label.text







