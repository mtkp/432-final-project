#!/usr/bin/python

import pygame
import inputbox
#import listbox
from pygame.locals import *    

# 
def print_error(message, fontObj, screenObj):
    label = fontObj.render(message, 1, (255,255,255))
    screenObj.blit(label, (100, 100))

def main():
    #client = GameClient()

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption('Basic Pygame program')

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
        break        

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


#------------------------------set up start screen----------------------------
    # Fill background
    font = pygame.font.Font(None, 36)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((195, 195, 195))

    # Display greeting text
    greeting = font.render("Hello There, User", 1, (10, 10, 10))
    greeting_pos = greeting.get_rect()
    greeting_pos.left = background.get_rect().left
    background.blit(greeting, greeting_pos)

    # make a rect for listbox to use
    list_box = pygame.Surface((250, 400))
    list_box.fill((0,0,0))
    list_box_pos = list_box.get_rect()
    list_box_pos.left = (background.get_rect().left + 20)
    list_box_pos.centery = background.get_rect().centery
    background.blit(list_box, list_box_pos)

    # setup the listbox title
    title_text = font.render("Active Users", 1, (10, 10, 10))
    title_text_pos = title_text.get_rect()
    title_text_pos.bottom = (list_box_pos.top)
    title_text_pos.left = (background.get_rect().left + 20)
    background.blit(title_text, title_text_pos)


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
