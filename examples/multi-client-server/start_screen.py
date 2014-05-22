#! /usr/bin/python

import socket

from Tkinter import *
import message

SERVER_PORT = 29717

class startwindow:

    def __init__(self, master):
        
        self.title_bar = Label( master, text="Game Title" )

        # buttons
        self.quit_button = Button( master, text="QUIT", command=master.quit )
        self.quit_button.grid(row=5, column=1)
        
        # should only be visible after connecting to server
        #self.listUsr_button = Button(master, text="List Users", command=self.list_users)
        #self.listUsr_button.grid(row=3, column=1)

        self.register_button = Button( master, text="Register", command=self.register )
        self.register_button.grid(row=1, column=1)

        # text entry boxes
        self.server_entry = Entry( master, width=50 )
        self.server_entry.grid(row=1, column=0)
        self.server_entry.insert(0, "server name" )

        self.user_entry = Entry( master, width=50 )
        self.user_entry.grid(row = 2, column = 0)
        self.user_entry.insert(0, "user name")
        
        # member variables
        self.username = ''
        self.command = ''
    
    # get server name from user and connect to it
    def register(self):
        server = self.server_entry.get()
        server = str(server)
        server += "\n"
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # now connect to the web server on port SERVER_PORT
        conn.connect((server, SERVER_PORT))

    # send username to server
    def send_username(self):
        self.username = self.user_entry.get()
        self.user_name += "\n"
        message.send_msg(conn, self.username)

    # send commands and receive response
    def list_users(self):
        message.send_msg(conn, "list")
        # receive list of users and print them out
        print message.recv_msg(conn)

    def join_game(self):
        print "TODO: implement join game"


root = Tk()
sw = startwindow(root)
root.mainloop()



#SERVER_PORT = 29717

# get server name from user
#server = raw_input("server: ")

#conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# now connect to the web server on port SERVER_PORT
#conn.connect((server, SERVER_PORT))
# send username to server
#name = raw_input("username: ")
#message.send_msg(conn, name)

# send commands and receive response
#command = ''
#while command != "exit" and command != "quit":
#    command = raw_input("command: ")
#    message.send_msg(conn, command)
#    print message.recv_msg(conn)

#conn.close()

