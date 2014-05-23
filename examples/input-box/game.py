#!/usr/bin/python

import pygame
import inputbox
#import listbox
from pygame.locals import *    

def print_error(message, fontObj, screenObj):
    label = fontObj.render(message, 1, (255,255,255))
    screenObj.blit(label, (100, 100))

def main():

    #client = GameClient()

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Basic Pygame program')

    # make a rect for listbox to use
    # 

    # setup text for error message
    myfont = pygame.font.SysFont("monospace", 15)   
    
    # get input, make connection
    while 1:
        server = inputbox.ask(screen, 'server')
        # check client side formatting
        print "joining server {}".format(server)
          
        username = inputbox.ask(screen, 'username')
        # check clientside formatting
        print "username {}".format(username)
        
        # take this out after importing gameclient
        print_error("error message", myfont, screen)
        
        #try:
        #    client.register(username, server, screen)
        #    break
        #except :
        #    print out error
        #    print_error("invalid usrname format", myfont, screen)

        #except :
        #    print out error
        #    print_error("user name taken", myfont, screen)

        #except :
        #    print out error
        #    print_error("server not found", myfont)
  
        # uncomment break after importing gameclient

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

    screen.blit(background, (0, 0))
    pygame.display.flip()


if __name__ == '__main__': main()
