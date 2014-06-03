#!/usr/bin/python2.7

# File:         util.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:
# Contains objects that are used to by pygame to display items on screen.  Box
# is a base object that the other classes inherit from.  Classes include 
# ListBox, which lists text items; TextBox, which is a Box that displays one 
# text item; InputBox, which takes user input, displays it and passes it too 
# the program; BorderBox which is a TextBox with a visible border; Label, which
# displays text whitout a visible box; and Button, which takes a mouseclick 
# event and triggers an event in the program.

# python modules
import itertools

# third party modules
import pygame

# our modules
from color import *

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


class BorderBox(object):
    def __init__(self, background, center, size, color, border_color=Black):
        self.border = Box(background, center, size, border_color)
        h, w = size
        size = h - 2, w - 2
        self.fill = Box(background, center, size, color)

    def draw(self):
        self.border.draw()
        self.fill.draw()

    def set_color(self, color):
        self.fill.set_color(color)

    def set_border_color(self, color):
        self.border.set_color(color)

    def collidepoint(self, xy):
        return self.border.collidepoint(xy)

    @property
    def center(self):
        return self.border.center

    @center.setter
    def center(self, center):
        self.border.center = center
        self.fill.center = center

    @property
    def centerx(self):
        return self.border.centerx

    @centerx.setter
    def centerx(self, centerx):
        self.border.centerx = centerx
        self.fill.centerx = centerx

    @property
    def centery(self):
        return self.border.centery

    @centery.setter
    def centery(self, centery):
        self.border.centery = centery
        self.fill.centery = centery

    @property
    def left(self):
        return self.border.left

    @left.setter
    def left(self, left):
        self.border.left = left
        self.fill.left = left + 1

    @property
    def right(self):
        return self.border.right

    @right.setter
    def right(self, right):
        self.border.right = right
        self.fill.right = right - 1

    @property
    def top(self):
        return self.border.top

    @top.setter
    def top(self, top):
        self.border.top = top
        self.fill.top = top + 1

    @property
    def bottom(self):
        return self.border.bottom

    @bottom.setter
    def bottom(self, bottom):
        self.border.bottom = bottom
        self.fill.bottom = bottom - 1

    @property
    def width(self):
        return self.border.width

    @width.setter
    def width(self, width):
        self.border.width = width
        self.fill.width = width - 2

    @property
    def height(self):
        return self.border.height

    @height.setter
    def height(self, height):
        self.border.height = height
        self.fill.height = height - 2

    @property
    def size(self):
        return self.border.size

    @size.setter
    def size(self, size):
        self.border.size = size
        h, w = size
        size = h - 2, w - 2
        self.fill.size = size


class Label(object):
    def __init__(self, background, center, font, text, color=Black):
        self.background = background
        self.font = font
        self.text = text
        self.center = center
        self.color = color
        self.text_rect = self.font.render(self.text, 1, self.color).get_rect()

    def draw(self):
        text_box = self.font.render(self.text, 1, self.color)
        self.text_rect = text_box.get_rect()
        self.text_rect.center = self.center
        self.background.blit(text_box, self.text_rect)

    @property
    def size(self):
        return self.text_rect.size

    def collidepoint(self, xy):
        return self.text_rect.collidepoint(xy)


class Button(object):
    def __init__(self, background, center, size, color, font, text):
        self.label = Label(background, center, font, text)
        self.box = BorderBox(background, center, size, color)

    def draw(self):
        self.box.draw()
        self.label.draw()

    def collidepoint(self, xy):
        return self.box.collidepoint(xy)


class InputBox(object):
    ascii_nums  = xrange(48, 58)
    ascii_chars = xrange(97, 123)
    ascii_misc  = [32, 45, 46] # space, dash, dot
    ascii_codes = itertools.chain(ascii_nums, ascii_chars, ascii_misc)
    allowed_input_keys = set(ascii_codes)

    def __init__(self, background, center, size, font, limit=20):
        self.label = Label(background, center, font, "")
        self.box = BorderBox(background, center, size, LightGray)
        self.active = False
        self.limit = limit

    def draw(self):
        if self.active:
            self.box.set_color(White)
        else:
            self.box.set_color(LightGray)
        self.box.draw()
        self.label.draw()

    def try_click(self, xy):
        self.active = self.collidepoint(xy)

    def collidepoint(self, xy):
        return self.box.collidepoint(xy)

    def input(self, raw):
        if raw in InputBox.allowed_input_keys:
            self.label.text += chr(raw)
            self.label.text = self.label.text[:self.limit]
        elif raw == pygame.K_BACKSPACE:
            self.label.text = self.label.text[0:-1]

    @property
    def text(self):
        return self.label.text

    def clear(self):
        self.label.text = ""


class TextBox(object):
    def align(func):
        def aligner(self, *args, **kwargs):
            return_val = func(self, *args, **kwargs)
            self.label.center = self.box.center
            return return_val
        return aligner

    def __init__(self, background, center, size, font, text=""):
        self.label = Label(background, center, font, text)
        self.box = BorderBox(background, center, size, White)

    def set_text_color(self, color):
        self.label.color = color

    def set_box_color(self, color):
        self.box.set_color(color)

    def draw(self):
        self.box.draw()
        self.label.draw()

    def collidepoint(self, xy):
        return self.box.collidepoint(xy)

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, text):
        self.label.text = text

    @property
    def center(self):
        return self.box.center

    @center.setter
    @align
    def center(self, center):
        self.box.center = center

    @property
    def centerx(self):
        return self.box.centerx

    @centerx.setter
    @align
    def centerx(self, centerx):
        self.box.centerx = centerx

    @property
    def centery(self):
        return self.box.centery

    @centery.setter
    @align
    def centery(self, centery):
        self.box.centery = centery

    @property
    def left(self):
        return self.box.left

    @left.setter
    @align
    def left(self, left):
        self.box.left = left

    @property
    def right(self):
        return self.box.right

    @right.setter
    @align
    def right(self, right):
        self.box.right = right

    @property
    def top(self):
        return self.box.top

    @top.setter
    @align
    def top(self, top):
        self.box.top = top

    @property
    def bottom(self):
        return self.box.bottom

    @bottom.setter
    @align
    def bottom(self, bottom):
        self.box.bottom = bottom

    @property
    def height(self):
        return self.box.height

    @height.setter
    @align
    def height(self, height):
        self.box.height = height


class ListBox(object):
    def __init__(self, background, center, size, font):
        self.background = background
        self.box = BorderBox(background, center, size, White)
        self.font = font
        self._list = []
        self.draw_list = []

    def draw(self):
        self.box.draw()
        for item in self.draw_list:
            item.draw()

    def collidepoint(self, xy):
        return self.box.collidepoint(xy)

    def get_item(self, xy):
        """Get the item at the specified xy coordinates
        """
        for item, label in zip(self._list, self.draw_list):
            if label.collidepoint(xy):
                return item

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, list):
        self._list = list
        self.build_draw_list()

    def build_draw_list(self):
        self.draw_list = []
        top = self.box.top
        centerx = self.box.centerx
        for i, item in enumerate(self._list):
            print "adding in {}".format(item)
            label = Label(
                self.background,
                (centerx, (top + 12) + (i * 24)),
                self.font,
                str(item))
            self.draw_list.append(label)




