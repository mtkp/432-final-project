#!/usr/bin/python

import pygame, sys
import inputbox
import gameclient

from pygame.locals import *    


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GRAY  = (195, 195, 195)

class Game(object):
    def __init__(self):
        self.client = gameclient.GameClient()
        self.users = []   
    
    def setup(self):
        self.error_font = pygame.font.SysFont("monospace", 15)
        self.label_font = pygame.font.Font(None, 36)
        self.user_font  = pygame.font.SysFont(None, 24)
              
    def _print_error(self, message):
        label = self.error_font.render(message, 1, RED)
        self.screen.blit(label, (100, 100))

    # diplay the username and server input boxes, get input
    def get_input(self):
        
    
    # use the username and servername to try to register w/ the server
    def try_register(self):
        try:
            client.register(username, server)
            break
        except gameclient.InvalidFormat:
            print_error("invalid usrname format")
        except gameclient.UsernameUnavailable:
            print_error("user name taken")
        except gameclient.ServerNotFound:
            print_error("server not found")

    def run(self):
        # strt pygame
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('CSS 432 Final Project')
    
    
        # get input, make connection
        while 1:
            server = inputbox.ask(screen, 'server')
            # TODO: check client side formatting of input here
            print "joining server {}".format(server)
              
            username = inputbox.ask(screen, 'username')
            # TODO: check clientside formatting
            print "username {}".format(username)        


#------------------------------set up start screen----------------------------

    # Fill main background with color
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((195, 195, 195))

    # Display greeting text at top of window
    greeting = label_font.render("Hello There", 1, (10, 10, 10))
    greeting_pos = greeting.get_rect()
    greeting_pos.left = background.get_rect().left
    background.blit(greeting, greeting_pos)

    # make a box to display users in
    user_box = pygame.Surface((250, 400))
    user_box.fill((255,255,255))
    user_box_pos = user_box.get_rect()
    user_box_pos.left = (background.get_rect().left + 20)
    user_box_pos.centery = background.get_rect().centery
    background.blit(user_box, user_box_pos)

    # setup the user box title
    title_text = label_font.render("Active Users", 1, (10, 10, 10))
    title_text_pos = title_text.get_rect()
    title_text_pos.bottom = (user_box_pos.top)
    title_text_pos.left = (background.get_rect().left + 20)
    background.blit(title_text, title_text_pos)
        
    # display users in users_box
    #users = client.get_users()
    user_names = []
    user_pos = []
    for i, name in enumerate(users):
        user_text = user_font.render(name, True, (10, 10, 10) )
        user_text_pos = user_text.get_rect()
        user_text_pos.left = (user_box_pos.left + 5)
        user_text_pos.top = user_box_pos.top + (i * (user_text_pos.height) + 2 )
        user_names.append(user_text)
        user_pos.append(user_text_pos)
        
    user_tups = zip(user_names, user_pos)
    for a, b in user_tups:      
        background.blit(a, b)
            
    # display everything to the screen
    screen.blit(background, (0, 0))
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
                for xy in user_pos:
                    if xy.collidepoint(pos):
                        print "you clicked on a name"

        screen.blit(background, (0, 0))
        pygame.display.flip()

         # Limit to 20 frames per second
        clock.tick(20)

if __name__ == '__main__': main()

