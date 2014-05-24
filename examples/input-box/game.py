#!/usr/bin/python

import pygame, sys
import inputbox
#import GameClient

from pygame.locals import *    

# 
def print_error(message, fontObj, screenObj):
    label = fontObj.render(message, 1, (255,255,255))
    screenObj.blit(label, (100, 100))

def main():
    #client = GameClient()

    # list of users eventually gotten from server
    users = ["Matt", "Greg", "Killroy", "Root"]

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption('Basic Pygame program')

    # setup text for error message
    error_font = pygame.font.SysFont("monospace", 15)   
    label_font = pygame.font.Font(None, 36)
    user_font = pygame.font.SysFont(None, 15)
    
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
        print_error("error message", error_font, screen)
        
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
    
    # Fill main background with color
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((195, 195, 195))

    # Display greeting text at top of window
    greeting = label_font.render("Hello There, User", 1, (10, 10, 10))
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

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

    screen.blit(background, (0, 0))
    pygame.display.flip()


if __name__ == '__main__': main()

