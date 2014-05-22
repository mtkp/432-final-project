#!/usr/bin/python2.7
# client

# python libs
import socket
import Tkinter as Tk

# our libs
import message
#import start_screen

SERVER_PORT = 29717

# event handler for register button
#def register():
#        print "TODO: implement register"

# event handler for list user button
#def list_users(self):
#        print "TODO: implement list users"

# event handler for join game button
#def join_game(self):
#        print "TODO: implement join game"

# the root of the Tk window
#root = Tk.Tk()

# a frame groups "widgets" like buttons and stuff
#frame = Tk.Frame(root)

# buttons for tk window
#title_label = Tk.Label(root, text="Game Title")
#title_label.pack()

#Quit_button = Tk.Button( frame, text="QUIT", command=frame.quit )
#Quit_button.pack()

#ListUsr_button = Tk.Button(frame, text="List Users", command=list_users)
#ListUsr_button.pack()

#Register_button = Tk.Button( frame, text="Register", command=register )
#Register_button.pack()


# start up the Tk window
#root. mainloop()


# get server name from user
server = raw_input("server: ")

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# now connect to the web server on port 7307
conn.connect((server, SERVER_PORT))

# send username to server
name = raw_input("username: ")
message.send_msg(conn, name)

# send commands and receive response
command = ''
while command != "exit" and command != "quit":
    command = raw_input("command: ")
    message.send_msg(conn, command)
    print message.recv_msg(conn)

conn.close()











