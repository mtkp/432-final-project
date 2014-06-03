#!/usr/bin/python2.7

# File:         start.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse
      
# Assignment:   Final Project

# Description:
# Start is the start screen view module that is displayed as soon as the 
# program.,py file is run.  It will display the title and prompt the user to 
# click the screen.  once the user clicks the screen, it sends an event to the
# event manager to transition the program state to the login screen.

import pygame

import base
import color
import util


class Start(base.Module):
    def __init__(self, handler, model):
        base.Module.__init__(self, handler, model)
        self.background_color = color.GameBackground
        self.font = pygame.font.SysFont("monospace", 60)

        label = util.Label(
            self.background,
            (self.width / 2, 200),
            self.font,
            "type it"
            )
        help_label = util.Label(
            self.background,
            (self.width / 2, 400),
            pygame.font.SysFont("monospace", 30),
            "click anywhere to begin"
            )
        self.draw_set.extend([
            label,
            help_label
            ])
