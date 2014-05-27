#!/usr/bin/python2.7

import pygame, sys

import listbox
import inputbox2
import gameclient

from pygame.locals import *    


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GRAY  = (195, 195, 195)

LIST_BOX_DIMS = (150, 200)

class Game2(object):
    def __init__(self):
        self.client = gameclient.GameClient()
        self.user_names = []
        self.user_tups  = []
        self.game_names = []
        self.game_tups  = []
    

    # setup different font objects 
    def setup_fonts(self):
        "setup some different fonts for later use"
        self.error_font = pygame.font.SysFont("monospace", 15)
        self.label_font = pygame.font.Font(None, 36)
        self.user_font  = pygame.font.SysFont(None, 24)


    ## get a list of tuples, used to display user list in listbox
    #def get_user_tups(self, user_boxes, user_pos):
    #    "get a list of tuples representing users"
    #    self.user_tups = zip(user_names, user_boxes, user_pos)
    #    return self.user_tups

    
    # display latest list of active users inside the active user listbox
    def refresh_users(self):
        "Refresh list of active users."
        # get up to date list of users
        self.user_names = self.client.get_users()
        self.user_tups = self.user_box.display_items(self.user_names)
        print "updated user list"

    # display latest list of active users inside the game listbox
    def refresh_games(self):
        "Refresh list of active games."
        # get up to date list of users
        self.games = self.client.get_games()
        self.game_tups = self.game_box.display_items(self.game_names)
        print "updated games list"

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
        self.BOTTOM_EDGE = self.background.get_rect().bottom
        self.LEFT_MARGIN = 5
        self.MARGIN = 5


    # make two listboxes, one for users and one for games
    def setup_listboxes(self):
        "instantiate a listbox for active users and games to join"
        
        # add a listbox to display active users in
        self.user_box = listbox.ListBox(self.background, WHITE, 
                            LIST_BOX_DIMS[0], LIST_BOX_DIMS[1],
                            self.LEFT_EDGE + self.LEFT_MARGIN, 
                            self.TOP_EDGE + 100)
        
        # add listbox to display games to join in
        self.game_box = listbox.ListBox(self.background, WHITE, 
                            LIST_BOX_DIMS[0], LIST_BOX_DIMS[1], 
                            self.LEFT_EDGE + LIST_BOX_DIMS[0] +
                            self.MARGIN + self.LEFT_MARGIN, 
                            self.TOP_EDGE + 100)

        # prepare to display on the screen
        #self.user_box.display_items(self.users)
        #self.game_box.display_items(self.users)

        # Display refresh button for user listbox
        self.user_refresh = self.label_font.render("refresh", True, (10, 10, 10))
        self.user_refresh_pos = self.user_refresh.get_rect()
        self.user_refresh_pos.top = self.user_box.box_surface_pos.bottom
        self.background.blit(self.user_refresh, self.user_refresh_pos)


    # setup input text boxes to get info from user
    def setup_textboxes(self):
        # server input box
        self.server_input_box = \
                inputbox2.InputBox2(self.background, WHITE, 
                                     200, 20, self.LEFT_EDGE + self.MARGIN, 
                                     self.BOTTOM_EDGE - self.MARGIN,
                                     "server", 1)

        # user input box
        self.user_input_box = \
                inputbox2.InputBox2(self.background, WHITE, 
                                     200, 20, self.LEFT_EDGE + self.MARGIN, 
                                     self.BOTTOM_EDGE, 
                                     "user", 2)

        #self.inputbox_buttons.append(self.server_input_box.box_surface_pos)
        #self.inputbox_buttons.append(self.user_input_box.box_surface_pos)


    # display red error message if something goes wrong w/ server or username
    def _print_error(self, message):
        "print a red error message to the screen if register operation fails"
        label = self.error_font.render(message, 1, RED)
        self.screen.blit(label, (100, 100))


    # get input from the server input box, then the user input box
    def get_input(self):
        "get user input for server, username"
        set_server = False
        set_name = False

        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if self.user_input_box.box_surface_pos.collidepoint(mouse):
                        self.username = self.user_input_box.ask()
                        set_name = True
                        # TODO: check clientside formatting
                        print "username {}".format(self.username)    
                    elif self.server_input_box.box_surface_pos.collidepoint(mouse):
                        self.server = self.server_input_box.ask()
                        set_server = True
                        # TODO: check client side formatting of input here
                        print "joining server {}".format(self.server)
                   
                pygame.display.flip()            
            if set_server and set_name:
                break
    

    # use the username and servername to try to register w/ the server
    def try_register(self):
        """Attempt to use the username and the server info to register to a 
        server"""
        while 1:
            # attempt to get the username and server strings
            self.get_input()
            # attempt to connect with given username and server info
            try:
                self.client.register(self.username, self.server)
                break
            except gameclient.InvalidFormat:
                self.print_error("invalid usrname format")
            except gameclient.UsernameUnavailable:
                self.print_error("user name taken")
            except gameclient.ServerNotFound:
                self.print_error("server not found")


    # run the program
    def run(self):
        "Run the program to display the lobby screen."
        # strt pygame
        pygame.init()  
        self.setup_fonts()
        self.setup_main_window()
        self.setup_listboxes();
        self.setup_textboxes();
                
        # display everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # try to get the input before making a connection
        self.try_register()

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while 1:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    print "You pressed the left mouse button at (%d, %d)" % event.pos       
                    for user in self.user_tups:
                        if user[2].collidepoint(mouse):
                            print "you clicked on {}".format(user[0])
                    if self.user_refresh_pos.collidepoint(mouse):
                        self.refresh_users()

            # --- Game logic should go here

            # --- Drawing code should go here
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()


             # Limit to 20 frames per second
            clock.tick(20)

        # close window and quit
        pygame.quit()

