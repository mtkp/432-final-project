#!/usr/bin/python

# libs
import pygame
from pygame.locals import *
import inputbox

# our libs
import gameclient


def print_error(message, font, screen):
    label = font.render(message, 1, (255,0,0))
    screen.blit(label, (100, 100))


def main():
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('CSS 432 Final Project')

    # fonts
    error_font = pygame.font.SysFont("monospace", 15)
    label_font = pygame.font.Font(None, 36)
    user_font  = pygame.font.SysFont(None, 20)

    with gameclient.GameClient() as client:

        # ----------------------- login screen ----------------------------
        while True:
            server = inputbox.ask(screen, 'server')
            # TODO: check client side formatting of input here
            print "joining server {}".format(server)

            username = inputbox.ask(screen, 'username')
            # TODO: check clientside formatting
            print "username {}".format(username)

            try:
                client.register(username, server)
                break
            except gameclient.InvalidFormat:
                print_error("invalid usrname format", error_font, screen)
            except gameclient.UsernameUnavailable:
                print_error("user name taken", error_font, screen)
            except gameclient.ServerNotFound:
                print_error("server not found", error_font, screen)


        # ---------------------- start screen ---------------------------
        # Fill main background with color
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((195, 195, 195))

        # Display greeting text at top of window
        greeting = label_font.render("Hello There", True, (10, 10, 10))
        greeting_pos = greeting.get_rect()
        greeting_pos.left = background.get_rect().left
        background.blit(greeting, greeting_pos)

        # make a box to display users in
        user_box = pygame.Surface((250, 250))
        user_box.fill((255,255,255))
        user_box_pos = user_box.get_rect()
        user_box_pos.left = (background.get_rect().left + 20)
        user_box_pos.centery = background.get_rect().centery
        background.blit(user_box, user_box_pos)

        # setup the user box title
        title_text = label_font.render("Active Users", True, (10, 10, 10))
        title_text_pos = title_text.get_rect()
        title_text_pos.bottom = (user_box_pos.top)
        title_text_pos.left = (background.get_rect().left + 20)
        background.blit(title_text, title_text_pos)

        # display users in users_box
        users = client.get_users()
        user_names = []
        user_pos = []
        for i, name in enumerate(users):
            user_text = user_font.render(name, True, (10, 10, 10), user_box.get_at((0,0)))
            user_text_pos = user_text.get_rect()
            user_text_pos.left = (user_box_pos.left + 5)
            user_text_pos.top = user_box_pos.top + (i * (user_text_pos.height) + 2)
            user_names.append(user_text)
            user_pos.append(user_text_pos)

        user_tups = zip(users, user_names, user_pos)
        for _, box, position in user_tups:
            background.blit(box, position)

        # display everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for user in user_tups:
                        if user[2].collidepoint(pygame.mouse.get_pos()):
                            print "you clicked on {}".format(user[0])

            # --- Game logic should go here

            # --- Drawing code should go here

            screen.blit(background, (0, 0))
            pygame.display.flip()

             # Limit to 20 frames per second
            clock.tick(30)

        # close window and quit
        pygame.quit()

if __name__ == '__main__':
    main()

