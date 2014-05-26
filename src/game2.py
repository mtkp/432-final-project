#!/usr/bin/python2.7

import pygame, sys
import listbox
import gameclient

from pygame.locals import *    


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GRAY  = (195, 195, 195)

LIST_BOX_DIMS = (250, 400)

class Game2(object):
    def __init__(self):
        self.client = gameclient.GameClient()
        self.users  = []
    

    # setup different font objects 
    def setup_fonts(self):
        "setup some different fonts for later use"
        self.error_font = pygame.font.SysFont("monospace", 15)
        self.label_font = pygame.font.Font(None, 36)
        self.user_font  = pygame.font.SysFont(None, 24)


    # setup for the lobby window
    def setup_main_window(self):
        "setup the lobby screen window"
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('CSS 432 Final Project')

        # Fill main background with color
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(GRAY)
        
        # Display greeting text at top of window
        self.greeting = self.label_font.render("Hello There", 1, (10, 10, 10))
        self.greeting_pos = self.greeting.get_rect()
        self.greeting_pos.left = self.background.get_rect().left
        self.background.blit(self.greeting, self.greeting_pos)

        self.TOP_EDGE  = self.background.get_rect().top
        self.LEFT_EDGE = self.background.get_rect().left


    def setup_listboxes(self):
        "instantiate a listbox for active users and games to join"
        # make two listboxes, one for users and one for games
        
        self.user_box = listbox.ListBox(self.background, WHITE, 
                            LIST_BOX_DIMS[0], LIST_BOX_DIMS[1],
                            self.LEFT_EDGE + 5, self.TOP_EDGE + 100)

        self.game_box = listbox.ListBox(self.background, WHITE, 
                            LIST_BOX_DIMS[0], LIST_BOX_DIMS[1], 
                            self.LEFT_EDGE + LIST_BOX_DIMS[0], 
                            self.TOP_EDGE + 100)


    # display red error message if something goes wrong w/ server or username
    def _print_error(self, message):
        "print a red error message to the screen if register operation fails"
        label = self.error_font.render(message, 1, RED)
        self.screen.blit(label, (100, 100))


    # diplay the username and server input boxes, get input
    def get_input(self):
        "get user input for server, username"
        while 1:
            self.server = inputbox.ask(screen, 'server')
            # TODO: check client side formatting of input here
            print "joining server {}".format(self.server)
              
            self.username = inputbox.ask(screen, 'username')
            # TODO: check clientside formatting
            print "username {}".format(self.username)        
    

    # use the username and servername to try to register w/ the server
    def try_register(self):
        """Attempt to use the username and the server info to register to a 
        server"""
        while 1:
            try:
                client.register(username, server)
                break
            except gameclient.InvalidFormat:
                print_error("invalid usrname format")
            except gameclient.UsernameUnavailable:
                print_error("user name taken")
            except gameclient.ServerNotFound:
                print_error("server not found")


    # run the program
    def run(self):
        "Run the program to display the lobby screen."
        # strt pygame
        pygame.init()  
        self.setup_fonts()
        self.setup_main_window()
        self.setup_listboxes();
        #get_input()
        #try_register   

        # setup the user box title
        #title_text = label_font.render("Active Users", 1, (10, 10, 10))
        #title_text_pos = title_text.get_rect()
        #title_text_pos.bottom = (user_box_pos.top)
        #title_text_pos.left = (background.get_rect().left + 20)
        #background.blit(title_text, title_text_pos)
                
        # display everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    print "You pressed the left mouse button at (%d, %d)" % event.pos
                    #for xy in self.user_pos:
                    #    if xy.collidepoint(pos):
                    #        print "you clicked on a name"

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

             # Limit to 20 frames per second
            clock.tick(20)

